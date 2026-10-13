import json
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from agents_board.model import Board, BoardError, StaleFile, file_version, split_entries
from agents_board.server import make_handler, render_page

ISSUES = """# Pytania

### W1. 🔴 Skala
- **Problem:** coś.
- **Propozycja:** tak.
- **Decyzja:**

### W2. 🟡 Inna
- **Problem:** x
- **Decyzja:** Zgoda

## Stan
"""

TODO = """# WAŻNE

- [ ] **A1. Pierwsze** opis
  ciąg dalszy
- [x] **A2. Drugie**
"""

TALK = """Zasady.

---
---
---

# Pytanie autora

treść

---
---
---

# Re: Pytanie autora

odpowiedź

*2026-10-14 01:15 — Claude Opus 5.5*

---
---
---
"""


@pytest.fixture
def root(tmp_path: Path) -> Path:
    r = tmp_path / "AGENTS"
    (r / "phases" / "phase-x").mkdir(parents=True)
    (r / "todo" / "author").mkdir(parents=True)
    (r / "talk").mkdir(parents=True)
    (r / "phases" / "phase-x" / "agents-issues-0.md").write_text(ISSUES)
    (r / "todo" / "author" / "WAZNE-TODO-dla-autora.md").write_text(TODO)
    (r / "todo" / "author" / "raport-TODO-autora.md").write_text("Raport\n\n---\n")
    (r / "talk" / "wymiana-zdan-A1.md").write_text(TALK)
    (r / "talk" / "od-autora-dla-llmow.md").write_text("Uwagi:\n\n1. Pierwsza.\n")
    return r


def test_parse(root):
    b = Board(root)
    issues = {i.extra["id"]: i for i in b.issues()}
    assert issues["W1"].status == "open" and issues["W2"].extra["decision"] == "Zgoda"
    todos = {t.extra["id"]: t for t in b.todos()}
    assert todos["A1"].status == " " and "ciąg dalszy" in todos["A1"].text and todos["A1"].group == "Ważne"
    talk = b.talk()
    assert [t.owner for t in talk] == ["author", "author", "llm"]
    assert talk[-1].title == "Re: Pytanie autora"
    st = b.state()
    assert st["waiting"]["issues"] == [issues["W1"].key] and st["waiting"]["talk"] == [talk[-1].key]


def test_split_entries_handles_consecutive_separators():
    entries = split_entries("a\n---\n---\n---\n---\n---\n---\n# b\nx\n")
    assert [e[1] for e in entries] == ["a", "# b\nx"]


def test_write_decision_once(root):
    b = Board(root)
    path = "phases/phase-x/agents-issues-0.md"
    b.write_decision(path, "W1", "Zgoda,\nale liniowo", file_version(root / path))
    text = (root / path).read_text()
    assert "- **Decyzja:** Zgoda,\n  ale liniowo\n" in text
    assert {i.extra["id"]: i.extra["decision"] for i in b.issues()}["W1"] == "Zgoda,\nale liniowo"
    with pytest.raises(BoardError, match="ma już decyzję"):
        b.write_decision(path, "W1", "inna", file_version(root / path))


def test_stale_version_is_rejected(root):
    b = Board(root)
    path = "phases/phase-x/agents-issues-0.md"
    old = file_version(root / path)
    (root / path).write_text(ISSUES + "\nzmiana w VS Code\n")
    with pytest.raises(StaleFile):
        b.write_decision(path, "W1", "x", old)


def test_status_report_talk_note(root):
    b = Board(root)
    todo = "todo/author/WAZNE-TODO-dla-autora.md"
    b.set_status(todo, "A1", "~", file_version(root / todo))
    assert "- [~] **A1. Pierwsze** opis" in (root / todo).read_text()

    rep = root / "todo/author/raport-TODO-autora.md"
    b.append_report("A1", "Pierwsze", "zrobione", file_version(rep))
    assert "### [A1] Pierwsze\n\nzrobione\n\n*" in rep.read_text() and rep.read_text().endswith("— Autor*\n\n---\n")

    talk = "talk/wymiana-zdan-A1.md"
    b.append_talk(talk, "Re: Re", "dzięki", file_version(root / talk))
    entries = split_entries((root / talk).read_text())
    assert entries[-1][1].startswith("# Re: Re\n\ndzięki") and len(entries) == 4
    assert b.talk()[-1].owner == "author"

    notes = root / "talk/od-autora-dla-llmow.md"
    b.append_note("Druga  uwaga", file_version(notes))
    assert notes.read_text().endswith("2. Druga uwaga\n")


def test_paths_outside_root_are_refused(root):
    with pytest.raises(BoardError):
        Board(root).resolve("../secret.md")


def test_page_embeds_config():
    html = render_page({"token": "t", "readOnly": True, "state": None}).decode()
    assert '"token": "t"' in html and "/*__CONFIG__*/" not in html


def test_server_requires_token(root):
    from http.server import ThreadingHTTPServer

    srv = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(Board(root), "secret", read_only=False))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    try:
        state = json.load(urllib.request.urlopen(base + "/api/state"))
        issue = next(i for i in state["issues"] if i["extra"]["id"] == "W1")
        body = json.dumps({"path": issue["path"], "id": "W1", "text": "Tak", "version": issue["version"]}).encode()

        req = urllib.request.Request(base + "/api/decision", data=body, method="POST")
        with pytest.raises(urllib.error.HTTPError) as e:
            urllib.request.urlopen(req)
        assert e.value.code == 403

        req = urllib.request.Request(base + "/api/decision", data=body, method="POST", headers={"X-Board-Token": "secret"})
        assert json.load(urllib.request.urlopen(req)) == {"ok": True}
        with pytest.raises(urllib.error.HTTPError) as e:  # same version again -> file changed -> 409
            urllib.request.urlopen(urllib.request.Request(base + "/api/decision", data=body, method="POST",
                                                          headers={"X-Board-Token": "secret"}))
        assert e.value.code == 409
    finally:
        srv.shutdown()
