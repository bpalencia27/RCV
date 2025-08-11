"""Funciones de cálculo desacopladas del estado Reflex.

Separar la lógica permite:
 - Reutilizar en tests sin inicializar el framework.
 - Facilitar validación y futura optimización.
"""
from __future__ import annotations
from typing import List, Tuple


def calc_imc(peso: str, talla_cm: str) -> str:
    """Calcula IMC dado peso (kg) y talla (cm) retornando string formateado ó ''."""
    try:
        if not (peso and talla_cm):
            return ""
        p = float(peso)
        t_m = float(talla_cm) / 100.0
        if t_m <= 0:
            return ""
        return f"{p / (t_m * t_m):.1f}"
    except Exception:
        return ""


def calc_tfg(edad: str, peso: str, creatinina: str, sexo: str) -> str:
    """TFG Cockcroft-Gault simplificada (ml/min) como string ó '' si insuficiente."""
    try:
        if not (edad and peso and creatinina):
            return ""
        e = float(edad)
        p = float(peso)
        cr = float(creatinina)
        if cr <= 0:
            return ""
        tfg = ((140 - e) * p) / (72 * cr)
        if sexo.lower() == "f":
            tfg *= 0.85
        return f"{int(tfg)} ml/min"
    except Exception:
        return ""


def calc_riesgo(
    dx_dm: bool,
    dx_hta: bool,
    dx_erc: bool,
    ecv_establecida: bool,
    edad: str,
    tfg_display: str,
    rac: str,
    hba1c: str,
    ldl: str,
) -> Tuple[str, List[str], int]:
    """Devuelve (nivel, factores, meta_ldl)."""
    puntaje = 0
    factores: List[str] = []

    def add(cond: bool, pts: int, label: str):
        nonlocal puntaje
        if cond:
            puntaje += pts
            factores.append(label)

    add(dx_dm, 2, "Diabetes")
    add(dx_hta, 1, "HTA")
    add(dx_erc, 2, "ERC")
    add(ecv_establecida, 4, "ECV establecida")
    try:
        if edad and int(edad) > 65:
            puntaje += 2
            factores.append("Edad>65")
    except Exception:
        pass
    try:
        if tfg_display:
            tfg_val = int(tfg_display.split()[0])
            if tfg_val < 30:
                puntaje += 4
                factores.append("TFG<30")
            elif tfg_val < 60:
                puntaje += 2
                factores.append("TFG<60")
    except Exception:
        pass
    try:
        if rac:
            rac_val = float(rac)
            if rac_val > 30:
                puntaje += 2
                factores.append("RAC>30")
    except Exception:
        pass
    try:
        if dx_dm and hba1c and float(hba1c) > 8:
            puntaje += 1
            factores.append("HbA1c>8")
    except Exception:
        pass
    try:
        if ldl and float(ldl) > 160:
            puntaje += 1
            factores.append("LDL>160")
    except Exception:
        pass

    # Validación de completitud mínima (simplificada a presencia tfg_display)
    if not (edad and tfg_display and (dx_dm or dx_hta or dx_erc)):
        return "INCOMPLETO", ["Complete datos obligatorios y al menos un dx"], 70

    if puntaje >= 10:
        nivel = "MUY ALTO"
        meta_ldl = 55
    elif puntaje >= 5:
        nivel = "ALTO"
        meta_ldl = 70
    elif puntaje >= 2:
        nivel = "MODERADO"
        meta_ldl = 100
    else:
        nivel = "BAJO"
        meta_ldl = 115
    return nivel, factores, meta_ldl


__all__ = ["calc_imc", "calc_tfg", "calc_riesgo"]
