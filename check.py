"""Local checks for the front-page PNG and the copy step in main.py."""

import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENTRY = ROOT / "assets" / "entry.png"
PNG = b"\x89PNG\r\n\x1a\n"
LIMIT = 1024 * 1024


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def main() -> None:
    data = ENTRY.read_bytes()
    if data[:8] != PNG:
        fail("assets/entry.png is not a PNG")
    if data[12:16] != b"IHDR":
        fail("PNG is missing IHDR")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if (width, height) != (1024, 1024):
        fail(f"size is {width}x{height}, expected 1024x1024")
    if len(data) > LIMIT:
        fail(f"file is {len(data)} bytes, over 1 MiB")

    with tempfile.TemporaryDirectory() as tmp:
        env = os.environ.copy()
        env["MAKEFUN_OUTPUT_DIR"] = tmp
        hashes = []
        for _ in range(2):
            subprocess.run(
                [sys.executable, "-P", "-s", str(ROOT / "main.py")],
                check=True,
                env=env,
            )
            hashes.append(sha256(Path(tmp) / "entry.png"))
    original = sha256(ENTRY)
    if hashes[0] != hashes[1] or hashes[0] != original:
        fail(f"hash mismatch {hashes[0]} {hashes[1]} {original}")
    print("PASS")


if __name__ == "__main__":
    main()
