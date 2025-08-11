from __future__ import annotations
from typing import Any, Dict
from .labs import normalize_lab_name

# ParsedData estructura mínima
# patient: dict, labs: list[dict]

def parse_document(content: bytes, filename: str) -> Dict[str, Any]:
    # Simulación simple: no OCR real, devolver placeholder
    return {
        "patient": {"pseudo_id": filename.split('.')[0], "sexo": "M", "edad": 60},
        "labs": [
            {"nombre": normalize_lab_name("creatinina"), "valor": 1.1, "unidad": "mg/dL"}
        ],
    }
