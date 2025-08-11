from __future__ import annotations
from .models import Paciente

# Puntaje simplificado (placeholder):
# - Edad: >= 65 -> +2
# - LDL >= 160 -> +2, 130-159 -> +1
# - HbA1c >= 8 -> +2, 7-7.9 -> +1
# - PAS >= 140 -> +1, >=160 -> +2 (sustituye anterior)
# - Creatinina >= 1.3 -> +1


def calcula_puntaje(paciente: Paciente) -> int:
    score = 0

    if paciente.edad >= 65:
        score += 2

    # Buscar labs relevantes
    def last(nombre: str):
        labs = [l for l in paciente.labs if l.nombre == nombre]
        return max(labs, key=lambda x: x.fecha) if labs else None

    ldl = last("COLESTEROL LDL")
    if ldl:
        if ldl.valor >= 160:
            score += 2
        elif ldl.valor >= 130:
            score += 1

    hba1c = last("HEMOGLOBINA GLICOSILADA (HBA1C)")
    if hba1c:
        if hba1c.valor >= 8:
            score += 2
        elif hba1c.valor >= 7:
            score += 1

    pas = last("PRESION ARTERIAL SISTOLICA")
    if pas:
        if pas.valor >= 160:
            score += 2
        elif pas.valor >= 140:
            score += 1

    crea = last("CREATININA EN SUERO U OTROS")
    if crea and crea.valor >= 1.3:
        score += 1

    return score


__all__ = ["calcula_puntaje"]
