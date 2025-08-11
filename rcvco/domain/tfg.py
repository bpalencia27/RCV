from __future__ import annotations
from .models import Paciente

# Fórmula Cockcroft-Gault (ml/min):
# ((140 - edad) * peso(kg) * (0.85 si mujer)) / (72 * Cr)
# Se espera creatinina en mg/dL


def crcl_cockcroft_gault(paciente: Paciente, creatinina_mg_dl: float | None = None) -> float | None:
    if paciente.peso_kg is None:
        return None
    if creatinina_mg_dl is None:
        # buscar creatinina sérica
        labs = [l for l in paciente.labs if l.nombre == "CREATININA EN SUERO U OTROS"]
        if not labs:
            return None
        creatinina_mg_dl = sorted(labs, key=lambda x: x.fecha)[-1].valor
    if creatinina_mg_dl <= 0:
        return None
    factor_sexo = 0.85 if paciente.sexo == "F" else 1.0
    crcl = ((140 - paciente.edad) * paciente.peso_kg * factor_sexo) / (72 * creatinina_mg_dl)
    return round(crcl, 2)


__all__ = ["crcl_cockcroft_gault"]
