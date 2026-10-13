"""python -m agents_board [--read-only] [--port 8765] [--static out.html]"""

import argparse
import sys
import webbrowser
from pathlib import Path

from agents_board.model import BoardError
from agents_board.server import serve, write_static

DEFAULT_ROOT = Path(__file__).resolve().parents[1] / "AGENTS"


def main() -> int:
    p = argparse.ArgumentParser(prog="python -m agents_board", description=__doc__)
    p.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="AGENTS folder (default: the repository's)")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--read-only", action="store_true", help="view only, no answering")
    p.add_argument("--static", type=Path, help="write a standalone read-only HTML file and exit")
    p.add_argument("--no-open", action="store_true", help="do not open the browser")
    args = p.parse_args()
    try:
        if args.static:
            print(f"written {write_static(args.root, args.static)}")
            return 0
        server = serve(args.root, args.port, args.read_only)
    except (BoardError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    url = f"http://127.0.0.1:{args.port}/"
    print(f"AGENTS board: {url}  ({'read-only' if args.read_only else 'answering enabled'}; Ctrl+C to stop)")
    if not args.no_open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


sys.exit(main())
