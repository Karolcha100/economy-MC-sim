"""Read the AGENTS/ markdown files into a tree and write the author's answers back.

The .md files stay the source of truth; this module only relies on their conventions:
    TODO item       - [ ] **A12. title** rest of the line…   (indented lines continue the item)
    issue section   ### W1. 🔴 title  …  - **Decyzja:** text
    thread          talk/threads/T001-slug.md: header '# T001 · title', then entries separated by
                    three '---' lines, each ending with a signature '*YYYY-MM-DD HH:MM — who*'
                    optional header line '*Odgałęzienie od: T002*' (sub-thread); an entry starting with
                    '🔒' closes the thread
    archive         talk/wymiana-zdan-*.md: the old single conversation, read-only in the GUI
    briefing        talk/briefings/RRRR-MM-DD-HHMM.md: the agent's end-of-session summary (newest shown)
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
SEPARATOR = "---\n---\n---"
LLM_SIGNATURE_RE = re.compile(r"—\s*(Claude|GPT|Gemini|LLM|model)", re.IGNORECASE)
SIGNATURE_RE = re.compile(r"^\*\d{4}-\d{2}-\d{2} \d{2}:\d{2} — .+\*$")
THREAD_TITLE_RE = re.compile(r"^# (?P<id>T\d+) · (?P<title>.+)$")
PARENT_RE = re.compile(r"^\*Odgałęzienie od: (?P<parent>T\d+)\*$", re.MULTILINE)
CLOSED_MARK = "🔒"
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
                decision = ""
                if decision_idx is not None:
                    decision = section[decision_idx][len(DECISION_MARK):].strip()
                    decision += "".join("\n" + line.strip() for line in section[decision_idx + 1:]
                                        if line.startswith("  ") and line.strip())
                m = ISSUE_RE.match(lines[start])
                items.append(Item(
                    key=f"issue:{self.rel(path)}:{m['id']}", kind="issue", title=f"{m['id']}. {m['title']}",
                    path=self.rel(path), line=start + 1, text="\n".join(section).rstrip(),
                    status="answered" if decision else ("open" if decision_idx is not None else "no-field"),
                    owner="author", group=path.parent.name, version=file_version(path),
                    extra={"id": m["id"], "decision": decision, "file": path.name},
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
                "issues": [i.key for i in issues if i.status == "open"],
                "todos": [t.key for t in todos if t.owner == "author" and t.status in OPEN_STATUSES],
                "threads": [t.key for t in waiting_threads],
            },
            "versions": {
                "report": file_version(self.root / "todo" / "author" / "raport-TODO-autora.md"),
                "notes": file_version(notes_path),
            },
            "statuses": STATUSES,
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

    def append_note(self, text: str, version: str) -> None:
        text = " ".join(text.split())
        if not text:
            raise BoardError("Pusta uwaga.")
        path = self.root / "talk" / "od-autora-dla-llmow.md"
        content = _check_version(path, version).rstrip()
        numbers = [int(m) for m in re.findall(r"^(\d+)\. ", content, re.MULTILINE)]
        content += f"\n\n{max(numbers, default=0) + 1}. {text}\n"
        _write_atomic(path, content)
