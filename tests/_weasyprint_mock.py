"""Install a WeasyPrint stub when native libraries are unavailable (test-only)."""

import sys
from unittest.mock import MagicMock

sys.modules.setdefault("weasyprint", MagicMock())
