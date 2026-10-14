import json
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from agents_board.model import Board, BoardError, StaleFile, ascii_slug, file_version, split_entries
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


THREAD = """# T001 · Pytanie

*Wątek.*

---
---
---

Pytanie autora

*2026-10-14 01:00 — Autor*

---
---
---

Odpowiedź

*2026-10-14 01:05 — Claude Opus 5.5*

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
    (r / "talk" / "threads").mkdir()
    (r / "talk" / "threads" / "T001-pytanie.md").write_text(THREAD)
    (r / "talk" / "od-autora-dla-llmow.md").write_text("Uwagi:\n\n1. Pierwsza.\n")
    return r


def test_parse(root):
    b = Board(root)
    issues = {i.extra["id"]: i for i in b.issues()}
    assert issues["W1"].status == "open" and issues["W2"].extra["decision"] == "Zgoda"
    todos = {t.extra["id"]: t for t in b.todos()}
    assert todos["A1"].status == " " and "ciąg dalszy" in todos["A1"].text and todos["A1"].group == "Ważne"
    threads = {t.extra["id"]: t for t in b.threads()}
    t1, archive = threads["T001"], threads["wymiana-zdan-A1"]
    assert t1.title == "Pytanie" and [e["owner"] for e in t1.extra["entries"]] == ["author", "llm"]
    assert t1.extra["entries"][1]["signature"] == "2026-10-14 01:05 — Claude Opus 5.5"
    assert archive.extra["archive"] and len(archive.extra["entries"]) == 3
    st = b.state()
    assert st["waiting"]["issues"] == [issues["W1"].key] and st["waiting"]["threads"] == [t1.key]


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

    thread = "talk/threads/T001-pytanie.md"
    b.append_thread(thread, "dzięki", file_version(root / thread))
    t1 = next(t for t in b.threads() if t.extra["id"] == "T001")
    assert t1.owner == "author" and t1.extra["entries"][-1]["text"].startswith("dzięki")
    with pytest.raises(BoardError, match="archiwum"):
        b.append_thread("talk/wymiana-zdan-A1.md", "x", file_version(root / "talk/wymiana-zdan-A1.md"))

    new = b.create_thread("Forma wymiany zdań", "treść")
    assert new == "talk/threads/T002-forma-wymiany-zdan.md"
    t2 = next(t for t in b.threads() if t.extra["id"] == "T002")
    assert t2.title == "Forma wymiany zdań" and t2.extra["entries"][0]["owner"] == "author"
    assert ascii_slug("Łódź — źródła") == "lodz-zrodla"

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


def test_branch_close_and_briefings(root):
    b = Board(root)
    child = b.create_thread("Wzmianki", "treść", parent="T001")
    assert "*Odgałęzienie od: T001*" in (root / child).read_text()
    threads = {t.extra["id"]: t for t in b.threads()}
    assert threads["T002"].extra["parent"] == "T001" and not threads["T002"].extra["closed"]
    with pytest.raises(BoardError, match="nadrzędnego"):
        b.create_thread("x", "y", parent="../T001")

    t1 = "talk/threads/T001-pytanie.md"
    b.close_thread(t1, file_version(root / t1), "dzięki")
    t = next(x for x in b.threads() if x.extra["id"] == "T001")
    assert t.extra["closed"] and t.extra["entries"][-1]["text"].startswith("🔒 Wątek zamknięty. dzięki")
    assert t.key not in b.state()["waiting"]["threads"]  # closed threads never wait

    (root / "talk" / "briefings").mkdir()
    (root / "talk" / "briefings" / "2026-10-14-0100.md").write_text("stary")
    (root / "talk" / "briefings" / "2026-10-14-0200.md").write_text("nowy")
    assert [x["text"] for x in b.state()["briefings"]] == ["nowy", "stary"]


def test_state_includes_help():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        st = Board(Path(d)).state()
    assert "AGENTS board" in st["help"]


def test_koniec_writes_summary_and_prompt(root):
    res = Board(root).write_koniec(["A1. Pierwsze", "T001 · Pytanie"], note="dzięki")
    text = (root / res["path"]).read_text()
    assert res["path"].startswith("talk/koniec/") and "- A1. Pierwsze" in text and "dzięki" in text
    assert "AGENTS/" + res["path"] in res["prompt"]


def test_koniec_counts_author_entries_since_last_koniec(root):
    from agents_board.model import merge_answered
    b = Board(root)
    (root / "talk" / "koniec").mkdir()
    (root / "talk" / "koniec" / "2026-10-14-0100.md").write_text("stary koniec")
    assert b.last_koniec() == "2026-10-14 01:00"
    # T001: author entry 01:00 is not newer than the last Koniec, agent entries never count
    assert b.activity() == []
    b.append_thread("talk/threads/T001-pytanie.md", "dalej", file_version(root / "talk/threads/T001-pytanie.md"))
    b.create_thread("Nowy temat", "treść")
    b.append_report("A1", "Pierwsze", "uwaga", file_version(root / "todo/author/raport-TODO-autora.md"))
    act = b.activity()
    assert "T001 · Pytanie — odpowiedź w wątku" in act and "T002 · Nowy temat — nowy wątek" in act
    assert "A1. Pierwsze — wpis w raporcie" in act
    assert merge_answered(["A1. Pierwsze — status [x]"], act)[0] == "A1. Pierwsze — status [x]"
    assert len(merge_answered(["A1. Pierwsze — status [x]"], act)) == 3
    text = (root / b.write_koniec([])["path"]).read_text()
    assert "T002 · Nowy temat — nowy wątek" in text and "A1. Pierwsze" in text


def test_question_to_task_and_final_answer(root):
    b = Board(root)
    rel = "phases/phase-x/agents-issues-0.md"
    res = b.move_issue(rel, "W1", file_version(root / rel), "chyba tak", to_task=True, to_report=True)
    assert res["task"] == "A3"
    todo = (root / "todo/author/WAZNE-TODO-dla-autora.md").read_text()
    assert "- [ ] **A3. W1: 🔴 Skala** — z pytania @phase-x:W1" in todo
    assert todo.index("A3.") > todo.index("A2.")
    assert "### [A3] W1: 🔴 Skala" in (root / "todo/author/raport-TODO-autora.md").read_text()
    w1 = next(i for i in b.issues() if i.extra["id"] == "W1")
    assert w1.status == "in-progress" and w1.extra["task"] == "A3" and "wstępnie: chyba tak" in w1.extra["decision"]
    assert w1.key not in b.state()["waiting"]["issues"]

    b.request_proposal(rel, "W1", file_version(root / rel))
    assert next(i for i in b.issues() if i.extra["id"] == "W1").status == "in-progress"
    text = (root / rel).read_text().replace("- **Propozycja końcowa:** (czeka na agenta)", "- **Propozycja końcowa:** skala 0..100")
    (root / rel).write_text(text)
    w1 = next(i for i in b.issues() if i.extra["id"] == "W1")
    assert w1.status == "proposal" and w1.key in b.state()["waiting"]["issues"]
    b.answer_proposal(rel, "W1", False, file_version(root / rel), "za mało")
    assert next(i for i in b.issues() if i.extra["id"] == "W1").status == "in-progress"
    (root / rel).write_text((root / rel).read_text().replace("- **Propozycja końcowa:** ❌", "- **Propozycja końcowa:** nowa\n  ❌", 1))
    b.answer_proposal(rel, "W1", True, file_version(root / rel))
    w1 = next(i for i in b.issues() if i.extra["id"] == "W1")
    assert w1.status == "answered" and w1.extra["decision"].startswith("✅ nowa")
    assert "### W2." in (root / rel).read_text()   # the next question is untouched


def test_question_final_answer_by_author(root):
    b = Board(root)
    rel = "phases/phase-x/agents-issues-0.md"
    b.move_issue(rel, "W1", file_version(root / rel), "", to_task=False, to_report=True)
    assert "### [phase-x:W1]" in (root / "todo/author/raport-TODO-autora.md").read_text()
    b.final_answer(rel, "W1", "Tak, skala 0..100", file_version(root / rel))
    w1 = next(i for i in b.issues() if i.extra["id"] == "W1")
    assert w1.status == "answered" and w1.extra["decision"] == "✅ Tak, skala 0..100"
    with pytest.raises(BoardError, match="ma już decyzję"):
        b.move_issue(rel, "W1", file_version(root / rel))
