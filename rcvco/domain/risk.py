from __future__ import annotations
from .models import Paciente
from .scoring import calcula_puntaje

# Clasificación 4 pasos (placeholder simplificado):
# 1) Identificar muy alto: score >=6
# 2) Alto: score 4-5
# 3) Moderado: score 2-3
# 4) Bajo: score 0-1


CATEGORIAS = [
    (6, "Muy Alto"),
    (4, "Alto"),
    (2, "Moderado"),
    (0, "Bajo"),
]


def clasificar_riesgo_cv_4_pasos(paciente: Paciente) -> str:
    score = calcula_puntaje(paciente)
    for umbral, nombre in CATEGORIAS:
        if score >= umbral:
            return nombre
    return "Bajo"


def ascvd_ajustado(paciente: Paciente) -> float:
    # Placeholder: derivar de score * factor
    score = calcula_puntaje(paciente)
    # Supuesto: 5% base + 2% por punto
    return min(100.0, 5 + score * 2.0)


__all__ = ["clasificar_riesgo_cv_4_pasos", "ascvd_ajustado"]
