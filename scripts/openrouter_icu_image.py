#!/usr/bin/env python3
"""Compatibility wrapper for the renamed Youtoken image CLI."""
from youtoken_image import main

if __name__ == "__main__":
    raise SystemExit(main())
