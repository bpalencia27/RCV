"""Catálogos UI centralizados (PR1 esqueleto).

Las listas finales deben DERIVARSE del dominio (rcvco.domain.*) en PRs posteriores.
"""
from __future__ import annotations
from typing import List, Dict

# Factores de riesgo completos según protocolo 4 Pasos
FACTORES_RIESGO: List[str] = [
    "Hipertensión",
    "Diabetes Mellitus",
    "Tabaquismo",
    "Obesidad",
    "Dislipidemia", 
    "Enfermedad Renal Crónica",
    "Enfermedad Cardiovascular",
    "Presión Arterial ≥180/110",  
    "LDL >190 mg/dL",
]

# Factores potenciadores riesgo CV completos
POTENCIADORES_RIESGO: List[str] = [
    "Historial Familiar ECV Prematura (<55H/<65M)", 
    "VIH",
    "Artritis Reumatoide",
    "Psoriasis",
    "ITB <0.9",  # índice tobillo-brazo
    "Lp(a) ≥50 mg/dL",
    "PCR ≥2 mg/L",
    "RAC >30 mg/g",  # relación albumina/creatinina
    "Condiciones Adversas Mujer",
    "Condiciones Socioeconómicas Adversas"
]

# Mapeo completo de laboratorios (nombre -> unidad) según reglas ERC
LABS_MAP: Dict[str, str] = {
    "CREATININA EN SUERO U OTROS": "mg/dL",  # nombre estándar obligatorio
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
    "RAC": "mg/g",  # relación albúmina/creatinina
    "PARCIAL DE ORINA": "N/A",
    "MICROALBUMINURIA": "mg/24h",
    "DEPURACIÓN CREATININA 24H": "mL/min",
    "POTASIO": "mEq/L",
    "CALCIO": "mg/dL",
    "PCR": "mg/L",  # proteína C reactiva
    "LP(A)": "mg/dL",  # lipoproteína A
    "HBA1C": "%",  # alias común
}

# Frecuencia de labs por estadio (X-Y días) (mantener consistente)
LABS_FRECUENCIA: Dict[str, Dict[str, tuple[int, int]]] = {
    "PARCIAL DE ORINA": {"E1": (180,180), "E2": (180,180), "E3A": (180,180), "E3B": (180,180), "E4": (120,120)},
    "CREATININA EN SUERO U OTROS": {"E1": (180,180), "E2": (180,180), "E3A": (90,121), "E3B": (90,121), "E4": (60,93)},
    "GLUCOSA EN SUERO": {"E1": (180,180), "E2": (180,180), "E3A": (180,180), "E3B": (180,180), "E4": (60,60)},
    "COLESTEROL TOTAL": {"E1": (180,180), "E2": (180,180), "E3A": (180,180), "E3B": (180,180), "E4": (120,120)},
    "COLESTEROL LDL": {"E1": (180,180), "E2": (180,180), "E3A": (180,180), "E3B": (180,180), "E4": (180,180)},
    "TRIGLICÉRIDOS": {"E1": (180,180), "E2": (180,180), "E3A": (180,180), "E3B": (180,180), "E4": (120,120)},
    "HEMOGLOBINA GLICOSILADA (HBA1C)": {"E1": (180,180), "E2": (180,180), "E3A": (180,180), "E3B": (180,180), "E4": (120,120)},
    "RAC": {"E1": (180,180), "E2": (180,180), "E3A": (180,180), "E3B": (180,180), "E4": (180,180)},
    "HEMOGLOBINA": {"E1": (365,365), "E2": (365,365), "E3A": (365,365), "E3B": (365,365), "E4": (180,180)},
    "HEMATOCRITO": {"E1": (365,365), "E2": (365,365), "E3A": (365,365), "E3B": (365,365), "E4": (180,180)},
    "PTH": {"E1": (0,0), "E2": (0,0), "E3A": (365,365), "E3B": (365,365), "E4": (180,180)},
    "ALBÚMINA SÉRICA": {"E1": (0,0), "E2": (0,0), "E3A": (0,0), "E3B": (365,365), "E4": (365,365)},
    "FÓSFORO": {"E1": (0,0), "E2": (0,0), "E3A": (0,0), "E3B": (365,365), "E4": (365,365)},
    "DEPURACIÓN CREATININA 24H": {"E1": (365,365), "E2": (180,180), "E3A": (180,180), "E3B": (180,180), "E4": (90,90)},
}

# Conveniente para UI: 0 significa "NR" (no requerido)
# Al agendar: +7 días si revisión médica

__all__ = ["FACTORES_RIESGO", "POTENCIADORES_RIESGO", "LABS_MAP"]
