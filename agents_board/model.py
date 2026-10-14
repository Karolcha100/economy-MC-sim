"""Read the AGENTS/ markdown files into a tree and write the author's answers back.

The .md files stay the source of truth; this module only relies on their conventions:
    TODO item       - [ ] **A12. title** rest of the line…   (indented lines continue the item)
    issue section   ### W1. 🔴 title  …  - **Decyzja:** text
                    decision '⏳ w toku → @A43 …' = moved to a task (T019); '✅ …' = final answer;
                    optional '- **Propozycja końcowa:** …' = the agent's final proposal for the author to accept
    thread          talk/threads/T001-slug.md: header '# T001 · title', then entries separated by
                    three '---' lines, each ending with a signature '*YYYY-MM-DD HH:MM — who*'
                    optional header line '*Odgałęzienie od: T002*' (sub-thread); an entry starting with
                    '🔒' closes the thread
    archive         talk/wymiana-zdan-*.md: the old single conversation, read-only in the GUI
    briefing        talk/briefings/RRRR-MM-DD-HHMM.md: the agent's end-of-session summary (newest shown)
    koniec          talk/koniec/RRRR-MM-DD-HHMM.md: what the author answered, written by the [Koniec] button —
                    his GUI actions plus every entry signed '— Autor' after the previous Koniec
    mention         @T002, @A12, @L3, @phase-2:R1 — links to threads, tasks and questions
Every write checks a content hash taken when the page was rendered, so an answer never
overwrites a file that changed in the meantime (e.g. edited in VS Code).
"""

from __future__ import annotations

import hashlib
import os
import re
import tempfile
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

STATUSES = {" ": "do zrobienia", "~": "w toku", "x": "zrobione", "?": "czeka", ">": "przeniesione", "-": "porzucone"}
OPEN_STATUSES = {" ", "~", "?"}
PRIORITY_FILES = {"WAZNE": "Ważne", "SREDNIE": "Średnie", "MALE": "Małe"}

TODO_RE = re.compile(r"^- \[(?P<status>.)\] \*\*(?P<id>[AL]\d+)\.\s*(?P<title>.*?)\*\*(?P<rest>.*)$")
ISSUE_RE = re.compile(r"^### (?P<id>[A-Z]+\d+)\.\s*(?P<title>.*)$")
DECISION_MARK = "- **Decyzja:**"
PROPOSAL_MARK = "- **Propozycja końcowa:**"
PROPOSAL_WAITING = "(czeka na agenta)"
PROPOSAL_REJECTED = "❌"
IN_PROGRESS_MARK = "⏳"
PRIORITY_PREFIX = {"Ważne": "WAZNE", "Średnie": "SREDNIE", "Małe": "MALE"}
SEPARATOR = "---\n---\n---"
LLM_SIGNATURE_RE = re.compile(r"—\s*(Claude|GPT|Gemini|LLM|model)", re.IGNORECASE)
SIGNATURE_RE = re.compile(r"^\*\d{4}-\d{2}-\d{2} \d{2}:\d{2} — .+\*$")
THREAD_TITLE_RE = re.compile(r"^# (?P<id>T\d+) · (?P<title>.+)$")
PARENT_RE = re.compile(r"^\*Odgałęzienie od: (?P<parent>T\d+)\*$", re.MULTILINE)
CLOSED_MARK = "🔒"
REPORT_ENTRY_RE = re.compile(r"^### \[(?P<id>[A-Z]\d+)\] (?P<title>.+)$")
AUTHOR_SIGNATURE_RE = re.compile(r"^\*(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}) — Autor\*$")
ITEM_ID_RE = re.compile(r"^(?P<id>[A-Z][A-Za-z-]*\d+)\b")
HELP = Path(__file__).parent / "HELP.md"


class BoardError(Exception):
    """Shown to the user as-is."""


class StaleFile(BoardError):
    """The file changed since the page was loaded."""


# --- files -------------------------------------------------------------------------------

def file_version(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()[:12] if path.exists() else "missing"


def _write_atomic(path: Path, text: str) -> None:
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def _check_version(path: Path, version: str) -> str:
    text = path.read_text(encoding="utf-8")
    if file_version(path) != version:
        raise StaleFile(f"{path.name} zmienił się od otwarcia strony. Odśwież (twoja odpowiedź zostaje w szkicu).")
    return text


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def split_entries(text: str) -> list[tuple[int, str]]:
    """Split a conversation at every run of three '---' lines -> [(first line number, entry text)]."""
    lines = text.splitlines()
    entries, current, start, i = [], [], 1, 0
    while i < len(lines):
        if all(i + k < len(lines) and lines[i + k].strip() == "---" for k in range(3)):
            entries.append((start, current))
            current, i = [], i + 3
            start = i + 1
            continue
        current.append(lines[i])
        i += 1
    entries.append((start, current))
    out = []
    for first, chunk in entries:
        while chunk and not chunk[0].strip():
            chunk, first = chunk[1:], first + 1
        if "".join(chunk).strip():
            out.append((first, "\n".join(chunk).strip()))
    return out


def ascii_slug(text: str, limit: int = 50) -> str:
    """'Forma wymiany zdań' -> 'forma-wymiany-zdan' (no Polish letters in file names)."""
    text = unicodedata.normalize("NFKD", text.replace("ł", "l").replace("Ł", "L"))
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")[:limit].rstrip("-") or "watek"


def thread_header(thread_id: str, title: str, parent: str = "") -> str:
    return (f"# {thread_id} · {title}\n\n"
            + (f"*Odgałęzienie od: {parent}*\n\n" if parent else "")
            + 
            "*Wątek. Wpisy oddzielone trzema liniami `---`; każdy kończy się podpisem "
            "`*RRRR-MM-DD GG:MM — kto*`. Nowe wpisy tylko na końcu, wcześniejszych nie edytujemy.*")


def _field_text(section: list[str], mark: str) -> str:
    """'- **Decyzja:** text' plus its indented continuation lines -> text ('' if missing or empty)."""
    idx = next((k for k, line in enumerate(section) if line.startswith(mark)), None)
    if idx is None:
        return ""
    text = section[idx][len(mark):].strip()
    return text + "".join("\n" + line.strip() for line in section[idx + 1:] if line.startswith("  ") and line.strip())


def _issue_bounds(lines: list[str], issue_id: str) -> tuple[int, int]:
    start = next((i for i, line in enumerate(lines) if (m := ISSUE_RE.match(line)) and m["id"] == issue_id), None)
    if start is None:
        raise BoardError(f"Nie ma pytania {issue_id}")
    end = next((j for j in range(start + 1, len(lines)) if lines[j].startswith(("### ", "## "))), len(lines))
    return start, end


def _set_field(lines: list[str], issue_id: str, mark: str, text: str, after: str = DECISION_MARK) -> None:
    """Replace (or add after the `after` field) one '- **Field:**' line with its continuation lines."""
    start, end = _issue_bounds(lines, issue_id)
    first, *rest = (text.strip() or " ").splitlines()
    new = [f"{mark} {first}".rstrip()] + [f"  {r}" if r.strip() else "" for r in rest]
    idx = next((j for j in range(start, end) if lines[j].startswith(mark)), None)
    if idx is None:
        anchor = next((j for j in range(start, end) if lines[j].startswith(after)), None)
        if anchor is None:
            raise BoardError(f"{issue_id} nie ma pola {after}")
        idx = anchor + 1
        while idx < end and lines[idx].startswith("  "):
            idx += 1
        lines[idx:idx] = new
        return
    stop = idx + 1
    while stop < end and lines[stop].startswith("  "):
        stop += 1
    lines[idx:stop] = new


def merge_answered(*lists: list[str]) -> list[str]:
    """Join answer lists without repeating an item (same leading id: A35, T018, K1…; else same text)."""
    seen, out = set(), []
    for item in (x for lst in lists for x in lst):
        m = ITEM_ID_RE.match(item)
        key = m["id"] if m else item
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


# --- tree model --------------------------------------------------------------------------

@dataclass
class Item:
    key: str                 # unique id in the tree
    kind: str                # todo | issue | talk | file | note
    title: str
    path: str                # relative to AGENTS/
    line: int                # 1-based
    text: str                # full markdown shown in the detail panel
    status: str = ""
    owner: str = ""          # author | llm
    group: str = ""          # e.g. priority, phase
    version: str = ""
    extra: dict = field(default_factory=dict)


class Board:
    def __init__(self, root: Path):
        self.root = Path(root)
        if not self.root.is_dir():
            raise BoardError(f"Brak folderu {self.root}")

    def rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def resolve(self, rel: str) -> Path:
        path = (self.root / rel).resolve()
        if self.root.resolve() not in path.parents:
            raise BoardError(f"Ścieżka poza AGENTS/: {rel}")
        if path.suffix != ".md" or not path.exists():
            raise BoardError(f"Nie ma pliku {rel}")
        return path

    # --- parsing ---------------------------------------------------------------------
    def todos(self) -> list[Item]:
        items = []
        for path in sorted(self.root.glob("todo/*/*.md")):
            owner = "author" if path.parent.name == "author" else "llm"
            group = next((label for key, label in PRIORITY_FILES.items() if path.name.startswith(key)), "")
            lines = path.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines):
                m = TODO_RE.match(line)
                if not m:
                    continue
                body = [line]
                for nxt in lines[i + 1:]:
                    if TODO_RE.match(nxt) or nxt.startswith("#") or (nxt and not nxt.startswith(" ")):
                        break
                    body.append(nxt)
                items.append(Item(
                    key=f"todo:{m['id']}:{self.rel(path)}", kind="todo", title=m["title"].strip(),
                    path=self.rel(path), line=i + 1, text="\n".join(body).rstrip(), status=m["status"],
                    owner=owner, group=group or "Agenci", version=file_version(path), extra={"id": m["id"]},
                ))
        return items

    def issues(self) -> list[Item]:
        items = []
        for path in sorted(self.root.glob("phases/*/agents-issues-*.md")):
            lines = path.read_text(encoding="utf-8").splitlines()
            starts = [i for i, line in enumerate(lines) if ISSUE_RE.match(line)]
            for n, start in enumerate(starts):
                end = len(lines)
                for j in range(start + 1, len(lines)):
                    if lines[j].startswith("### ") or lines[j].startswith("## "):
                        end = j
                        break
                section = lines[start:end]
                decision_idx = next((k for k, line in enumerate(section) if line.startswith(DECISION_MARK)), None)
                decision = _field_text(section, DECISION_MARK)
                proposal = _field_text(section, PROPOSAL_MARK)
                if decision_idx is None:
                    status = "no-field"
                elif not decision:
                    status = "open"
                elif decision.startswith(IN_PROGRESS_MARK):
                    ready = proposal and not proposal.startswith((PROPOSAL_WAITING, PROPOSAL_REJECTED))
                    status = "proposal" if ready else "in-progress"
                else:
                    status = "answered"
                m = ISSUE_RE.match(lines[start])
                items.append(Item(
                    key=f"issue:{self.rel(path)}:{m['id']}", kind="issue", title=f"{m['id']}. {m['title']}",
                    path=self.rel(path), line=start + 1, text="\n".join(section).rstrip(),
                    status=status, owner="author", group=path.parent.name, version=file_version(path),
                    extra={"id": m["id"], "decision": decision, "proposal": proposal, "file": path.name,
                           "task": (t["id"] if (t := re.search(r"@(?P<id>A\d+)", decision)) else "")},
                ))
        return items

    def threads(self) -> list[Item]:
        """Conversation threads (talk/threads/) plus old conversation files as read-only archives."""
        items = []
        paths = [(p, False) for p in sorted(self.root.glob("talk/threads/T*.md"))]
        paths += [(p, True) for p in sorted(self.root.glob("talk/wymiana-zdan-*.md"))]
        for path, archive in paths:
            parts = split_entries(path.read_text(encoding="utf-8"))
            if not parts:
                continue
            header_line, header = parts[0]
            m = THREAD_TITLE_RE.match(header.splitlines()[0]) if not archive else None
            entries = []
            for line_no, body in (parts if archive else parts[1:]):
                last = body.splitlines()[-1]
                title_line = next((x for x in body.splitlines() if x.startswith("# ")), None)
                entries.append({
                    "line": line_no, "text": body,
                    "owner": "llm" if LLM_SIGNATURE_RE.search(last) else "author",
                    "title": (title_line[2:].strip() if title_line else body.splitlines()[0].strip())[:90],
                    "signature": last.strip("* ") if SIGNATURE_RE.match(last.strip()) else "",
                })
            thread_id = m["id"] if m else path.stem
            title = m["title"].strip() if m else f"Archiwum: {path.stem}"
            parent = PARENT_RE.search(header)
            closed = archive or any(e["text"].lstrip().startswith(CLOSED_MARK) for e in entries)
            items.append(Item(
                key=f"thread:{self.rel(path)}", kind="thread", title=title, path=self.rel(path),
                line=header_line, text=header, owner=entries[-1]["owner"] if entries else "author",
                group="archive" if archive else "threads", version=file_version(path),
                extra={"id": thread_id, "entries": entries, "archive": archive, "closed": closed,
                       "parent": parent["parent"] if parent else ""},
            ))
        return items

    def briefings(self) -> list[dict]:
        """Agent briefings, newest first: [{name, text}]."""
        folder = self.root / "talk" / "briefings"
        return [{"name": p.stem, "path": self.rel(p), "text": p.read_text(encoding="utf-8")}
                for p in sorted(folder.glob("*.md"), reverse=True)] if folder.exists() else []

    def last_koniec(self) -> str:
        """'YYYY-MM-DD HH:MM' of the newest [Koniec] summary, '' if none."""
        folder = self.root / "talk" / "koniec"
        stems = sorted(p.stem for p in folder.glob("*.md")) if folder.exists() else []
        if not stems or not re.fullmatch(r"\d{4}-\d{2}-\d{2}-\d{4}", stems[-1]):
            return ""
        s = stems[-1]
        return f"{s[:10]} {s[11:13]}:{s[13:15]}"

    def activity(self, since: str | None = None) -> list[str]:
        """What the author wrote in the files since the last [Koniec] (signed '— Autor'), also outside the GUI:
        thread entries (new thread / reply / closing) and entries in raport-TODO-autora.md."""
        since = self.last_koniec() if since is None else since
        out = []
        for t in self.threads():
            if t.extra["archive"]:
                continue
            entries = t.extra["entries"]
            new = [e for e in entries if e["owner"] == "author" and e["signature"][:16] > since]
            if not new:
                continue
            if entries and entries[0] in new:
                what = "nowy wątek"
            elif any(e["text"].lstrip().startswith(CLOSED_MARK) for e in new):
                what = "zamknięty"
            else:
                what = "odpowiedź w wątku"
            out.append(f"{t.extra['id']} · {t.title} — {what}")
        report = self.root / "todo" / "author" / "raport-TODO-autora.md"
        if report.exists():
            for body in re.split(r"\n---[ \t]*\n", report.read_text(encoding="utf-8")):
                lines = body.splitlines()
                head = next((m for line in lines if (m := REPORT_ENTRY_RE.match(line))), None)
                sig = next((m for line in reversed(lines) if (m := AUTHOR_SIGNATURE_RE.match(line.strip()))), None)
                if head and sig and sig["date"] > since:
                    out.append(f"{head['id']}. {head['title'].strip()} — wpis w raporcie")
        return out

    def files(self) -> list[Item]:
        return [
            Item(key=f"file:{self.rel(p)}", kind="file", title=self.rel(p), path=self.rel(p), line=1,
                 text=p.read_text(encoding="utf-8"), group=p.parent.relative_to(self.root).as_posix() or ".",
                 version=file_version(p))
            for p in sorted(self.root.rglob("*.md"))
        ]

    def state(self) -> dict:
        todos, issues, threads = self.todos(), self.issues(), self.threads()
        waiting_threads = [t for t in threads if not t.extra["closed"] and t.owner == "llm"]
        notes_path = self.root / "talk" / "od-autora-dla-llmow.md"
        return {
            "root": str(self.root),
            "generated": now(),
            "todos": [asdict(t) for t in todos],
            "issues": [asdict(i) for i in issues],
            "threads": [asdict(t) for t in threads],
            "files": [asdict(f) for f in self.files()],
            "briefings": self.briefings(),
            "help": HELP.read_text(encoding="utf-8") if HELP.exists() else "",
            "waiting": {
                "issues": [i.key for i in issues if i.status in ("open", "proposal")],
                "todos": [t.key for t in todos if t.owner == "author" and t.status in OPEN_STATUSES],
                "threads": [t.key for t in waiting_threads],
            },
            "versions": {
                "report": file_version(self.root / "todo" / "author" / "raport-TODO-autora.md"),
                "notes": file_version(notes_path),
            },
            "statuses": STATUSES,
            "since": self.last_koniec(),
            "activity": self.activity(),
        }

    # --- writing ---------------------------------------------------------------------
    def write_decision(self, rel: str, issue_id: str, text: str, version: str) -> None:
        text = text.strip()
        if not text:
            raise BoardError("Pusta decyzja.")
        path = self.resolve(rel)
        lines = _check_version(path, version).split("\n")
        start = next((i for i, line in enumerate(lines)
                      if (m := ISSUE_RE.match(line)) and m["id"] == issue_id), None)
        if start is None:
            raise BoardError(f"Nie ma pytania {issue_id} w {rel}")
        for j in range(start + 1, len(lines)):
            if lines[j].startswith("### ") or lines[j].startswith("## "):
                break
            if lines[j].startswith(DECISION_MARK):
                if lines[j][len(DECISION_MARK):].strip():
                    raise BoardError(f"{issue_id} ma już decyzję — dopisz zmianę ręcznie w pliku.")
                first, *rest = text.splitlines()
                lines[j:j + 1] = [f"{DECISION_MARK} {first}"] + [f"  {r}" if r.strip() else "" for r in rest]
                _write_atomic(path, "\n".join(lines))
                return
        raise BoardError(f"{issue_id} nie ma pola Decyzja.")

    def set_status(self, rel: str, todo_id: str, status: str, version: str) -> None:
        if status not in STATUSES:
            raise BoardError(f"Nieznany status {status!r}")
        path = self.resolve(rel)
        lines = _check_version(path, version).split("\n")
        for i, line in enumerate(lines):
            m = TODO_RE.match(line)
            if m and m["id"] == todo_id:
                lines[i] = f"- [{status}]" + line[5:]
                _write_atomic(path, "\n".join(lines))
                return
        raise BoardError(f"Nie ma zadania {todo_id} w {rel}")

    def append_report(self, todo_id: str, title: str, text: str, version: str) -> None:
        text = text.strip()
        if not text:
            raise BoardError("Pusty wpis.")
        path = self.root / "todo" / "author" / "raport-TODO-autora.md"
        content = _check_version(path, version).rstrip("\n")
        if not content.endswith("---"):
            content += "\n\n---"
        content += f"\n\n### [{todo_id}] {title.strip()}\n\n{text}\n\n*{now()} — Autor*\n\n---\n"
        _write_atomic(path, content)

    def append_thread(self, rel: str, text: str, version: str) -> None:
        """Add the author's entry at the end of a thread."""
        text = text.strip()
        if not text:
            raise BoardError("Pusty wpis.")
        if not rel.startswith("talk/threads/"):
            raise BoardError("Można pisać tylko w wątkach (talk/threads/); stara wymiana zdań to archiwum.")
        path = self.resolve(rel)
        content = _check_version(path, version).rstrip()
        if not content.endswith(SEPARATOR):
            content += "\n\n" + SEPARATOR
        content += f"\n\n{text}\n\n*{now()} — Autor*\n\n{SEPARATOR}\n"
        _write_atomic(path, content)

    def close_thread(self, rel: str, version: str, note: str = "") -> None:
        """The author closes a thread: an entry starting with 🔒."""
        text = f"{CLOSED_MARK} Wątek zamknięty." + (f" {note.strip()}" if note.strip() else "")
        self.append_thread(rel, text, version)

    def create_thread(self, title: str, text: str, parent: str = "") -> str:
        """Start a new thread file (optionally branched from another thread); returns its path."""
        title, text, parent = " ".join(title.split()), text.strip(), parent.strip()
        if not title or not text:
            raise BoardError("Potrzebny tytuł i treść.")
        if parent and not re.fullmatch(r"T\d+", parent):
            raise BoardError(f"Zły numer wątku nadrzędnego: {parent!r}")
        folder = self.root / "talk" / "threads"
        folder.mkdir(parents=True, exist_ok=True)
        numbers = [int(m.group(1)) for p in folder.glob("T*.md") if (m := re.match(r"T(\d+)", p.name))]
        thread_id = f"T{max(numbers, default=0) + 1:03d}"
        path = folder / f"{thread_id}-{ascii_slug(title)}.md"
        _write_atomic(path, thread_header(thread_id, title, parent)
                      + f"\n\n{SEPARATOR}\n\n{text}\n\n*{now()} — Autor*\n\n{SEPARATOR}\n")
        return self.rel(path)

    # --- question -> task / report (T019) ------------------------------------------------
    def _issue_lines(self, rel: str, version: str) -> tuple[Path, list[str]]:
        path = self.resolve(rel)
        if not path.name.startswith("agents-issues-"):
            raise BoardError("To nie jest plik pytań.")
        return path, _check_version(path, version).split("\n")

    def next_author_task_id(self) -> str:
        ids = [int(m["id"][1:]) for p in self.root.glob("todo/author/*.md")
               for line in p.read_text(encoding="utf-8").splitlines()
               if (m := TODO_RE.match(line)) and m["id"].startswith("A")]
        return f"A{max(ids, default=0) + 1}"

    def move_issue(self, rel: str, issue_id: str, version: str, preliminary: str = "",
                   to_task: bool = True, to_report: bool = True, priority: str = "Ważne") -> dict:
        """Open question -> new author task and/or report entry; the question shows '⏳ w toku → @A…'."""
        if not (to_task or to_report):
            raise BoardError("Wybierz zadanie, raport albo oba.")
        path, lines = self._issue_lines(rel, version)
        start, end = _issue_bounds(lines, issue_id)
        if _field_text(lines[start:end], DECISION_MARK):
            raise BoardError(f"{issue_id} ma już decyzję.")
        title = ISSUE_RE.match(lines[start])["title"].strip()
        mention = f"@{path.parent.name}:{issue_id}"
        preliminary = preliminary.strip()
        ref = ""
        if to_task:
            if priority not in PRIORITY_PREFIX:
                raise BoardError(f"Nieznany priorytet {priority!r}")
            task_file = next(self.root.glob(f"todo/author/{PRIORITY_PREFIX[priority]}*.md"), None)
            if task_file is None:
                raise BoardError(f"Brak pliku zadań {PRIORITY_PREFIX[priority]}")
            ref = self.next_author_task_id()
            tlines = task_file.read_text(encoding="utf-8").split("\n")
            last = max((i for i, line in enumerate(tlines) if TODO_RE.match(line)), default=len(tlines) - 1)
            while last + 1 < len(tlines) and tlines[last + 1].startswith("  "):
                last += 1
            tlines.insert(last + 1, f"- [ ] **{ref}. {issue_id}: {title}** — z pytania {mention}"
                                    f" (`{self.rel(path)}`). *(dodane {now()})*")
            _write_atomic(task_file, "\n".join(tlines))
        if to_report:
            report = self.root / "todo" / "author" / "raport-TODO-autora.md"
            self.append_report(ref or f"{path.parent.name}:{issue_id}", f"{issue_id}: {title}",
                               preliminary or "(bez wstępnej odpowiedzi)", file_version(report))
        target = f"@{ref}" if ref else "raport"
        _set_field(lines, issue_id, DECISION_MARK, f"{IN_PROGRESS_MARK} w toku → {target}"
                   + (f" (wstępnie: {preliminary})" if preliminary else ""))
        _write_atomic(path, "\n".join(lines))
        return {"task": ref}

    def final_answer(self, rel: str, issue_id: str, text: str, version: str) -> None:
        """The author closes a question that was in progress with his own final answer."""
        text = text.strip()
        if not text:
            raise BoardError("Pusta odpowiedź.")
        path, lines = self._issue_lines(rel, version)
        start, end = _issue_bounds(lines, issue_id)
        decision = _field_text(lines[start:end], DECISION_MARK)
        ref = re.search(r"@(A\d+)", decision)
        _set_field(lines, issue_id, DECISION_MARK, f"✅ {text}" + (f" (po @{ref[1]})" if ref else ""))
        _write_atomic(path, "\n".join(lines))

    def request_proposal(self, rel: str, issue_id: str, version: str) -> None:
        path, lines = self._issue_lines(rel, version)
        _set_field(lines, issue_id, PROPOSAL_MARK, PROPOSAL_WAITING)
        _write_atomic(path, "\n".join(lines))

    def answer_proposal(self, rel: str, issue_id: str, accept: bool, version: str, comment: str = "") -> None:
        """Accept the agent's final proposal (-> decision ✅) or reject it with a comment (back to 'w toku')."""
        path, lines = self._issue_lines(rel, version)
        start, end = _issue_bounds(lines, issue_id)
        proposal = _field_text(lines[start:end], PROPOSAL_MARK)
        if not proposal or proposal.startswith((PROPOSAL_WAITING, PROPOSAL_REJECTED)):
            raise BoardError(f"{issue_id} nie ma propozycji do oceny.")
        if accept:
            decision = _field_text(lines[start:end], DECISION_MARK)
            ref = re.search(r"@(A\d+)", decision)
            _set_field(lines, issue_id, DECISION_MARK,
                       f"✅ {proposal} (propozycja agenta zaakceptowana{f', po @{ref[1]}' if ref else ''})")
        else:
            _set_field(lines, issue_id, PROPOSAL_MARK, f"{PROPOSAL_REJECTED} odrzucona {now()}"
                       + (f": {comment.strip()}" if comment.strip() else "") + f"\n(poprzednia: {proposal})")
        _write_atomic(path, "\n".join(lines))

    def write_koniec(self, answered: list[str], note: str = "") -> dict:
        """The author pressed [Koniec]: write what was answered this session and return a prompt for the agent."""
        folder = self.root / "talk" / "koniec"
        folder.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d-%H%M")
        path = folder / f"{stamp}.md"
        lines = [f"# Koniec sesji autora — {now()}", "",
                 "Autor skończył odpowiadać w AGENTS board. Na co odpowiedział w tej sesji:", ""]
        answered = merge_answered(answered, self.activity())
        lines += [f"- {item}" for item in answered] or ["- (GUI nie wykrył zmian — sprawdź wątki i pytania)"]
        if note.strip():
            lines += ["", "Uwaga autora:", "", note.strip()]
        lines += ["", f"*{now()} — Autor (przycisk Koniec)*", ""]
        _write_atomic(path, "\n".join(lines))
        rel = self.rel(path)
        prompt = (f"Odpowiedziałem w AGENTS board. Podsumowanie: AGENTS/{rel} "
                  f"({len(answered)} pozycji). Przeczytaj je i kontynuuj według AGENTS/todo/llm/INSTRUKCJA.md.")
        return {"path": rel, "prompt": prompt}

    def append_note(self, text: str, version: str) -> None:
        text = " ".join(text.split())
        if not text:
            raise BoardError("Pusta uwaga.")
        path = self.root / "talk" / "od-autora-dla-llmow.md"
        content = _check_version(path, version).rstrip()
        numbers = [int(m) for m in re.findall(r"^(\d+)\. ", content, re.MULTILINE)]
        content += f"\n\n{max(numbers, default=0) + 1}. {text}\n"
        _write_atomic(path, content)
