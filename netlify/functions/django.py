"""
Netlify Functions — Django ASGI (Mangum).
"""
import os
import sys

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_FN = os.path.dirname(os.path.abspath(__file__))
if _FN not in sys.path:
    sys.path.insert(0, _FN)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "naron.settings_netlify")

from django.core.asgi import get_asgi_application  # noqa: E402
from mangum import Mangum  # noqa: E402

_django_asgi = get_asgi_application()
handler = Mangum(_django_asgi, lifespan="off")
