#!/usr/bin/env python3
"""Entry program for news-image-20261124.

Copies the front-page image this repository ships (entry.png, drawn by
render.py in this same session) to the output directory, as entry.png.
Standard library only; no network; deterministic — both runs write the
same bytes.
"""
import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        sys.exit("entry.png missing next to main.py")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    assert size <= 1048576, f"entry.png too large: {size} bytes"
    print("wrote", dst, size, "bytes")


if __name__ == "__main__":
    main()
