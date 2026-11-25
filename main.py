#!/usr/bin/env python3

import os
import shutil
from pathlib import Path

def main():
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    src_path = Path(__file__).resolve().parent / "assets" / "entry.png"
    shutil.copyfile(src_path, output_dir / "entry.png")

if __name__ == "__main__":
    main()
