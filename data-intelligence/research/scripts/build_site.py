#!/usr/bin/env python3
"""Build the generated site from canonical Markdown sources.

Usage (from the repository root):

    python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
    .venv/bin/python scripts/build_site.py

Output is written to ``site/``. Generated HTML is disposable presentation:
canonical Markdown always takes precedence.
"""

import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep the repository free of __pycache__
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sitegen.build import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
