"""Emit the canonical, offline competition image using only the standard library."""
import os
from pathlib import Path


def main():
    art = Path(__file__).resolve().with_name("artwork.png")
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    (out / "entry.png").write_bytes(art.read_bytes())


if __name__ == "__main__":
    main()
