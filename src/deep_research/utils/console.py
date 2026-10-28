from __future__ import annotations

import sys
from rich.console import Console

# Safely reconfigure standard streams on Windows to prevent GBK/cp936 encoding errors
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Global safe console
console = Console(safe_box=True)
