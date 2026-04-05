#!/usr/bin/env python3
"""Generate website assets (pack icon, favicon) from the resource pack generator."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from generate_pack import generate_pack_png

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "website")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Pack icon for website
    pack_icon = generate_pack_png()
    pack_icon.save(os.path.join(OUTPUT_DIR, "pack-icon.png"), "PNG")
    print("Generated pack-icon.png")

    # Favicon (32x32 version)
    favicon = pack_icon.resize((32, 32))
    favicon.save(os.path.join(OUTPUT_DIR, "favicon.png"), "PNG")
    print("Generated favicon.png")


if __name__ == "__main__":
    main()
