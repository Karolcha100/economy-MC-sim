"""Read the AGENTS/ markdown files into a tree and write the author's answers back.

The .md files stay the source of truth; this module only relies on their conventions:
    TODO item       - [ ] **A12. title** rest of the line…   (indented lines continue the item)
    issue section   ### W1. 🔴 title  …  - **Decyzja:** text
    conversation    entries separated by three '---' lines, each starting with '# title'
Every write checks a content hash taken when the page was rendered, so an answer never
overwrites a file that changed in the meantime (e.g. edited in VS Code).
"""

from __future__ import annotations

import hashlib
import os
import re
import tempfile
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

    def talk(self) -> list[Item]:
        items = []
        for path in sorted(self.root.glob("talk/wymiana-zdan-*.md")):
            for k, (line_no, body) in enumerate(split_entries(path.read_text(encoding="utf-8"))):
                title_line = next((line for line in body.splitlines() if line.startswith("# ")), None)
                title = title_line[2:].strip() if title_line else ("Zasady pliku" if k == 0 else body.splitlines()[0][:60])
                last = body.splitlines()[-1]
                items.append(Item(
                    key=f"talk:{self.rel(path)}:{line_no}", kind="talk", title=title, path=self.rel(path),
                    line=line_no, text=body, owner="llm" if LLM_SIGNATURE_RE.search(last) else "author",
                    group=path.stem, version=file_version(path),
                ))
        return items

    def files(self) -> list[Item]:
        return [
            Item(key=f"file:{self.rel(p)}", kind="file", title=self.rel(p), path=self.rel(p), line=1,
                 text=p.read_text(encoding="utf-8"), group=p.parent.relative_to(self.root).as_posix() or ".",
                 version=file_version(p))
            for p in sorted(self.root.rglob("*.md"))
        ]

    def state(self) -> dict:
        todos, issues, talk = self.todos(), self.issues(), self.talk()
        last_talk = {}
        for t in talk:
            last_talk[t.path] = t
        waiting_talk = [t for t in last_talk.values() if t.owner == "llm"]
        notes_path = self.root / "talk" / "od-autora-dla-llmow.md"
        return {
            "root": str(self.root),
            "generated": now(),
            "todos": [asdict(t) for t in todos],
            "issues": [asdict(i) for i in issues],
            "talk": [asdict(t) for t in talk],
            "files": [asdict(f) for f in self.files()],
            "waiting": {
                "issues": [i.key for i in issues if i.status == "open"],
                "todos": [t.key for t in todos if t.owner == "author" and t.status in OPEN_STATUSES],
                "talk": [t.key for t in waiting_talk],
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

    def append_talk(self, rel: str, title: str, text: str, version: str) -> None:
        title, text = title.strip(), text.strip()
        if not title or not text:
            raise BoardError("Potrzebny tytuł i treść.")
        path = self.resolve(rel)
        content = _check_version(path, version).rstrip()
        if not content.endswith(SEPARATOR):
            content += "\n\n" + SEPARATOR
        content += f"\n\n# {title}\n\n{text}\n\n*{now()} — Autor*\n\n{SEPARATOR}\n"
        _write_atomic(path, content)

    def append_note(self, text: str, version: str) -> None:
        text = " ".join(text.split())
        if not text:
            raise BoardError("Pusta uwaga.")
        path = self.root / "talk" / "od-autora-dla-llmow.md"
        content = _check_version(path, version).rstrip()
        numbers = [int(m) for m in re.findall(r"^(\d+)\. ", content, re.MULTILINE)]
        content += f"\n\n{max(numbers, default=0) + 1}. {text}\n"
        _write_atomic(path, content)
