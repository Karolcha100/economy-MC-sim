"""Local web server for the AGENTS board (standard library only).

Listens on 127.0.0.1 only. Every write request must carry the per-run token embedded in the page,
so other websites open in the browser cannot post to it.
"""

from __future__ import annotations

import json
import secrets
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from agents_board.model import Board, BoardError, StaleFile

PAGE = Path(__file__).parent / "static" / "index.html"


def render_page(config: dict) -> bytes:
    html = PAGE.read_text(encoding="utf-8")
    payload = json.dumps(config, ensure_ascii=False).replace("</", "<\\/")
    return html.replace("/*__CONFIG__*/null", payload).encode("utf-8")


def make_handler(board: Board, token: str, read_only: bool):
    actions = {
        "decision": lambda d: board.write_decision(d["path"], d["id"], d["text"], d["version"]),
        "status": lambda d: board.set_status(d["path"], d["id"], d["status"], d["version"]),
        "report": lambda d: board.append_report(d["id"], d["title"], d["text"], d["version"]),
        "thread": lambda d: board.append_thread(d["path"], d["text"], d["version"]),
        "new-thread": lambda d: {"path": board.create_thread(d["title"], d["text"], d.get("parent", ""))},
        "close-thread": lambda d: board.close_thread(d["path"], d["version"], d.get("text", "")),
        "note": lambda d: board.append_note(d["text"], d["version"]),
        "koniec": lambda d: board.write_koniec(list(d.get("answered", [])), d.get("note", "")),
    }

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):  # keep the terminal quiet
            pass

        def _send(self, status: int, body: bytes, ctype: str = "application/json; charset=utf-8") -> None:
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, status: int, data: dict) -> None:
            self._send(status, json.dumps(data, ensure_ascii=False).encode("utf-8"))

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                config = {"token": token, "readOnly": read_only, "state": None}
                self._send(HTTPStatus.OK, render_page(config), "text/html; charset=utf-8")
            elif self.path == "/api/state":
                try:
                    self._json(HTTPStatus.OK, board.state())
                except BoardError as e:
                    self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(e)})
            else:
                self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})

        def do_POST(self):
            action = self.path.removeprefix("/api/")
            if self.headers.get("X-Board-Token") != token:
                return self._json(HTTPStatus.FORBIDDEN, {"error": "Zły token — odśwież stronę."})
            if read_only:
                return self._json(HTTPStatus.FORBIDDEN, {"error": "Tryb tylko do odczytu."})
            if action not in actions:
                return self._json(HTTPStatus.NOT_FOUND, {"error": f"Nieznana akcja {action}"})
            try:
                length = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(length) or b"{}")
                result = actions[action](data)
            except StaleFile as e:
                return self._json(HTTPStatus.CONFLICT, {"error": str(e)})
            except (BoardError, KeyError, ValueError) as e:
                return self._json(HTTPStatus.BAD_REQUEST, {"error": str(e)})
            self._json(HTTPStatus.OK, {"ok": True, **(result if isinstance(result, dict) else {})})

    return Handler


def serve(root: Path, port: int = 8765, read_only: bool = False) -> ThreadingHTTPServer:
    board = Board(root)
    token = secrets.token_urlsafe(16)
    return ThreadingHTTPServer(("127.0.0.1", port), make_handler(board, token, read_only))


def write_static(root: Path, out: Path) -> Path:
    """Stage 1 viewer: one HTML file with the current state embedded, no server needed."""
    config = {"token": "", "readOnly": True, "state": Board(root).state()}
    out.write_bytes(render_page(config))
    return out
