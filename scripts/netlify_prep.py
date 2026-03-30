"""Build sırasında Django dosyalarını netlify/functions altına kopyalar (Netlify Linux)."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "netlify" / "functions"

APPS = [
    "naron",
    "accounts",
    "assignments",
    "assets",
    "core",
    "orders",
    "parameters",
    "products",
    "reports",
    "stock",
]
DIRS = ["templates", "static"]


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    for name in APPS + DIRS:
        src = ROOT / name
        if not src.exists():
            continue
        dst = DEST / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    sf = ROOT / "staticfiles"
    if sf.exists():
        dst = DEST / "staticfiles"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(sf, dst)


if __name__ == "__main__":
    main()
