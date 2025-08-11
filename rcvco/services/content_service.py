from __future__ import annotations
import json, os, threading
from typing import Any, Dict

_LOCK = threading.Lock()
_CONTENT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'editable_content.json')
_CONTENT_PATH = os.path.abspath(_CONTENT_PATH)

def _ensure_dir():
    d = os.path.dirname(_CONTENT_PATH)
    if not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)

DEFAULT_CONTENT: Dict[str, Any] = {
    "about_md": "## Acerca de\nContenido editable inicial.",
    "home_notice": "Bienvenido a la plataforma clínica.",
}

def load_content() -> Dict[str, Any]:
    _ensure_dir()
    if not os.path.isfile(_CONTENT_PATH):
        save_content(DEFAULT_CONTENT)
    try:
        with _LOCK, open(_CONTENT_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONTENT.copy()

def save_content(data: Dict[str, Any]) -> None:
    _ensure_dir()
    with _LOCK, open(_CONTENT_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
