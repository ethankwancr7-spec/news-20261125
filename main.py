"""Copy assets/entry.png into the make.fun output directory. Stdlib only."""

import os
import shutil
from pathlib import Path


def main() -> None:
    source = Path(__file__).resolve().parent / "assets" / "entry.png"
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"
    shutil.copyfile(source, destination)
    try:
        os.chmod(destination, 0o644)
    except OSError:
        pass


if __name__ == "__main__":
    main()
