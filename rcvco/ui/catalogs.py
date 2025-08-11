"""Catálogos UI centralizados (PR1 esqueleto).

Las listas finales deben DERIVARSE del dominio (rcvco.domain.*) en PRs posteriores.
"""
from __future__ import annotations
from typing import List, Dict

# Factores de riesgo (placeholder) — reemplazar con extracción de dominio
FACTORES_RIESGO: List[str] = [
    "Hipertensión",
    "Diabetes Mellitus",
    "Tabaquismo",
    "Obesidad",
]

POTENCIADORES_RIESGO: List[str] = [
    "Historial Familiar Prematuro",
    "ERC",
    "Inflamación Crónica",
]

# Mapeo básico de laboratorios (nombre -> unidad esperada) — derivar de dominio
LABS_MAP: Dict[str, str] = {
    "CREATININA EN SUERO U OTROS": "mg/dL",
    "HEMOGLOBINA GLICOSILADA (HBA1C)": "%",
    "COLESTEROL TOTAL": "mg/dL",
    "COLESTEROL LDL": "mg/dL",
    "COLESTEROL HDL": "mg/dL",
    "TRIGLICÉRIDOS": "mg/dL",
    "GLUCOSA EN SUERO": "mg/dL",
    "HEMOGLOBINA": "g/dL",
    "HEMATOCRITO": "%",
    "FÓSFORO": "mg/dL",
    "ALBÚMINA SÉRICA": "g/dL",
    "PTH": "pg/mL",
    "RAC": "mg/g",
}

__all__ = ["FACTORES_RIESGO", "POTENCIADORES_RIESGO", "LABS_MAP"]
