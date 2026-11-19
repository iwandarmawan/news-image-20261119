#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261119 bounty.

Copies the bundled front-page image (entry.png, drawn for Thursday
19 November 2026) to the output directory and checks it is a whole
PNG under the 1 MiB limit. Standard library only, no network, no
randomness, no timestamps: both runs write the same bytes.
"""
import hashlib
import os
import shutil
import sys

MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def output_dir():
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return env
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(os.getcwd(), "out")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    dest_dir = output_dir()
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "entry.png")
    shutil.copyfile(src, dest)
    with open(src, "rb") as f:
        src_hash = hashlib.sha256(f.read()).hexdigest()
    with open(dest, "rb") as f:
        dest_hash = hashlib.sha256(f.read()).hexdigest()
    if src_hash != dest_hash:
        print("copied entry.png does not match the bundled file",
              file=sys.stderr)
        return 1
    size = os.path.getsize(dest)
    if size > MAX_BYTES:
        print("entry.png is %d bytes, over the 1 MiB limit" % size,
              file=sys.stderr)
        return 1
    with open(dest, "rb") as f:
        head = f.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    with open(dest, "rb") as f:
        f.seek(16)
        width, height = int.from_bytes(f.read(4), "big"), int.from_bytes(
            f.read(4), "big")
    if width > 1024 or height > 1024:
        print("entry.png is %dx%d, over the 1024x1024 limit"
              % (width, height), file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, %dx%d)" % (dest, size, width, height))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
