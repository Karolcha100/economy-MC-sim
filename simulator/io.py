"""Shared file conventions: CSV format, slugs, atomic writes and scenario locks."""

from __future__ import annotations

import os
import re
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import pandas as pd

FLOAT_DECIMALS = 4
ENCODING = "utf-8"

_SLUG_INVALID = re.compile(r"[^a-z0-9-]")
_SLUG_DASHES = re.compile(r"-{2,}")


class SimulatorError(Exception):
    """Raised on any user/LLM input error. The message is meant to be shown as-is."""


def slugify(name: str) -> str:
    """Lowercase, spaces -> '-', drop everything outside [a-z0-9-]."""
    slug = name.strip().lower().replace(" ", "-")
    slug = _SLUG_INVALID.sub("", slug)
    slug = _SLUG_DASHES.sub("-", slug).strip("-")
    return slug


def read_csv(path: Path, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, encoding=ENCODING, **kwargs)


def write_csv(df: pd.DataFrame, path: Path, index: bool = True) -> None:
    """Write a CSV atomically (temp file + rename), rounding floats to FLOAT_DECIMALS."""
    path.parent.mkdir(parents=True, exist_ok=True)
    out = df.copy()
    float_cols = out.select_dtypes(include="float").columns
    out[float_cols] = out[float_cols].round(FLOAT_DECIMALS)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=ENCODING, newline="") as f:
            out.to_csv(f, index=index)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


@contextmanager
def file_lock(path: Path, timeout: float = 60.0, poll: float = 0.1) -> Generator[None]:
    """Exclusive lock based on O_EXCL file creation. Stale locks must be removed by hand."""
    deadline = time.monotonic() + timeout
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            if time.monotonic() > deadline:
                raise SimulatorError(
                    f"Could not acquire lock {path} within {timeout}s. "
                    "If no other process is writing, delete the lock file."
                )
            time.sleep(poll)
    try:
        os.write(fd, f"{os.getpid()}\n".encode())
        os.close(fd)
        yield
    finally:
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass
