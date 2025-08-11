from __future__ import annotations
from typing import Dict

# Mapping variantes -> canon
LAB_NAME_MAP: Dict[str, str] = {
    "creat": "CREATININA EN SUERO U OTROS",
    "creatinina": "CREATININA EN SUERO U OTROS",
    "crea": "CREATININA EN SUERO U OTROS",
}

def normalize_lab_name(raw: str) -> str:
    key = raw.strip().lower()
    return LAB_NAME_MAP.get(key, raw.strip().upper())
