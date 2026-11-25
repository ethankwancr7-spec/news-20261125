"""Emit twice, compare, validate the PNG, and refresh the local 300 px proof."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
from uuid import uuid4

from PIL import Image

ROOT = Path(__file__).resolve().parent


def emit(directory):
    directory.mkdir(exist_ok=True)
    subprocess.run(
        [sys.executable, "-B", "-S", str(ROOT / "main.py")],
        cwd=directory,
        env=dict(os.environ, MAKEFUN_OUTPUT_DIR=str(directory)),
        check=True,
    )
    return directory / "entry.png"


def verify():
    scratch = ROOT / (".verify-" + uuid4().hex)
    try:
        first = emit(scratch).read_bytes()
        path = emit(ROOT / "output")
        assert first == path.read_bytes() == (ROOT / "artwork.png").read_bytes()
        assert len(first) <= 1024**2
        with Image.open(path) as im:
            assert im.format == "PNG" and im.size == (1024, 1024)
            im.verify()
        with Image.open(path) as im:
            im.convert("RGB").resize((300, 300), Image.Resampling.LANCZOS).save(
                ROOT / "preview.png"
            )
        print(f"PASS: 1024 x 1024 PNG, {len(first):,} bytes; both runs match artwork.png")
        print("SHA-256:", hashlib.sha256(first).hexdigest())
    finally:
        (scratch / "entry.png").unlink(missing_ok=True)
        if scratch.exists():
            scratch.rmdir()


if __name__ == "__main__":
    verify()
