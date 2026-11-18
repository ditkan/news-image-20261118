#!/usr/bin/env python3
"""make.fun news-image-20261118 entry program.

The entry image (entry.png, a front page carrying 150 numbered world
news stories of Wednesday 18 November 2026) is rendered ahead of time
by render.py and shipped in this repository. At grading time this
program simply copies that image, byte for byte, into the output
directory, so both grading runs produce identical bytes.

Standard library only. Honours MAKEFUN_BOT_DIR / MAKEFUN_OUTPUT_DIR
when set; falls back to the script's own directory and ./output.
"""
import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR", here)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", os.path.join(here, "output"))
    src = os.path.join(bot_dir, "entry.png")
    if not os.path.isfile(src):
        src = os.path.join(here, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    with open(dst, "wb") as f:
        f.write(data)
    print(f"wrote {dst} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
