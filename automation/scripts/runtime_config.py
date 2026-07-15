from __future__ import annotations

import os
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DOTENV_CANDIDATES = (
    PROJECT_ROOT / ".env",
    SCRIPT_DIR / ".env",
)


def load_dotenv_like(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


def load_env() -> None:
    for candidate in DOTENV_CANDIDATES:
        load_dotenv_like(candidate)


def env(name: str, default: str) -> str:
    return os.getenv(name, default)
