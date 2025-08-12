"""Funciones de cálculo core desacopladas del estado Reflex.

Este módulo implementa las reglas clínicas principales:
- TFG por Cockcroft-Gault
- Clasificación riesgo CV (4 Pasos)
- Ajuste metas por programa
- IMC
"""
from __future__ import annotations
from typing import List, Tuple
from rcvco.ui.types import EstadioERC, RiesgoCV, Programa, Sexo

def calc_imc(peso_kg: float, talla_m: float) -> float:
    """Calcula IMC (kg/m²).
    
    Args:
        peso_kg: Peso en kilogramos
        talla_m: Talla en metros
    
    Returns:
        float: IMC en kg/m²
    """
    if peso_kg <= 0 or talla_m <= 0:
        return 0.0
    return round(peso_kg / (talla_m * talla_m), 1)

def calc_tfg_cg(
    edad: int,
    peso_kg: float,
    creatinina_mg_dl: float,
    sexo: str,
) -> float:
    """Calcula TFG usando Cockcroft-Gault.
    
    Args:
        edad: Edad en años
        peso_kg: Peso en kilogramos
        creatinina_mg_dl: Creatinina sérica en mg/dL
        sexo: 'M' masculino o 'F' femenino
    
    Returns:
        float: TFG en mL/min
    """
    if not all([edad > 0, peso_kg > 0, creatinina_mg_dl > 0]):
        return 0.0
        
    # Fórmula base: ((140 - edad) × peso) / (72 × Cr)
    tfg = ((140 - edad) * peso_kg) / (72 * creatinina_mg_dl)
    
    # Ajuste por sexo
    if sexo == Sexo.F:
        tfg *= 0.85
        
    return round(tfg, 1)


def get_estadio_erc(tfg: float) -> EstadioERC:
    """Determina estadio ERC según TFG.
    
    Args:
        tfg: TFG en mL/min
    
    Returns:
        EstadioERC: Estadio correspondiente
    """
    if tfg >= 90:
        return EstadioERC.E1
    elif tfg >= 60:
        return EstadioERC.E2
    elif tfg >= 45:
        return EstadioERC.E3A
    elif tfg >= 30:
        return EstadioERC.E3B
    elif tfg >= 15:
        return EstadioERC.E4
    else:
        return EstadioERC.E5

def calc_riesgo_cv_4_pasos(
    *,
    edad: int,
    sexo: str,
    has_ecv: bool = False,
    has_dm: bool = False,
    has_hta: bool = False,
    has_dislipidemia: bool = False,
    tfg: float | None = None,
    pa_sistolica: float | None = None,
    ldl: float | None = None,
    factores_riesgo: List[str] | None = None,
    potenciadores: List[str] | None = None,
) -> Tuple[RiesgoCV, str]:
    """Implementa protocolo 4 Pasos.
    
    Returns:
        Tuple[RiesgoCV, str]: (Categoría, justificación sin mencionar "pasos")
    """
    factores_riesgo = factores_riesgo or []
    potenciadores = potenciadores or []
    
    # Paso 1: Muy Alto
    if (
        has_ecv  # ECV establecida
        or (tfg and tfg <= 30)  # ERC severa
        or (  # DM con criterios
            has_dm
            and (
                len(factores_riesgo) >= 3  # ≥3 FR
                or any(p in potenciadores for p in [  # daño órgano
                    "RAC >30 mg/g",
                    "Retinopatía",
                    "Neuropatía"
                ])
            )
        )
    ):
        return (
            RiesgoCV.MUY_ALTO,
            "Riesgo muy alto por " + (
                "ECV establecida" if has_ecv
                else "ERC severa" if tfg and tfg <= 30
                else "DM con daño de órgano blanco o múltiples factores"
            )
        )

    # Paso 2: Alto
    if (
        (tfg and 30 < tfg <= 60)  # ERC moderada
        or (pa_sistolica and pa_sistolica >= 180)  # HTA severa
        or (ldl and ldl > 190)  # Dislipidemia severa
        or len(factores_riesgo) >= 3  # Múltiples FR
    ):
        return (
            RiesgoCV.ALTO,
            "Riesgo alto por " + (
                "ERC moderada" if tfg and 30 < tfg <= 60
                else "HTA severa" if pa_sistolica and pa_sistolica >= 180
                else "dislipidemia severa" if ldl and ldl > 190
                else "múltiples factores de riesgo"
            )
        )

    # Paso 3: Potenciadores
    n_potenciadores = len(potenciadores)
    if n_potenciadores >= 3:
        return (
            RiesgoCV.ALTO,
            "Riesgo alto por múltiples condiciones potenciadoras"
        )
    elif n_potenciadores > 0:
        return (
            RiesgoCV.MODERADO,
            "Riesgo moderado por presencia de condiciones potenciadoras"
        )

    # Paso 4: Por defecto Bajo
    return (
        RiesgoCV.BAJO,
        "Riesgo bajo por ausencia de criterios mayores"
    )
def get_metas_programa(
    *,
    programa: Programa,
    edad: int,
    has_ecv: bool = False,
    estadio: EstadioERC | None = None,
) -> Tuple[int, int, int, float]:
    """Determina metas según programa y condiciones.
    
    Args:
        programa: Programa prioritario (ERC/DM/HTA)
        edad: Edad en años
        has_ecv: Si tiene ECV establecida
        estadio: Estadio ERC actual
        
    Returns:
        Tuple[int, int, int, float]: (PA_sys, PA_dia, LDL, HbA1c)
    """
    # PA por edad (todos los programas)
    if edad >= 60:
        pa_sys, pa_dia = 150, 90
    else:
        pa_sys, pa_dia = 140, 90
        
    # LDL y HbA1c por programa
    if programa == Programa.ERC:
        if estadio and estadio == EstadioERC.E4:
            # E4: otros parámetros más importantes
            ldl = 130
            hba1c = 8.0 if has_ecv else 7.0
        else:
            # E1-E3: metas usuales
            ldl = 100
            hba1c = 7.0
            
    elif programa == Programa.DM:
        ldl = 100
        hba1c = 8.0 if (edad > 65 or has_ecv) else 7.0
        
    else:  # HTA
        ldl = 100 if has_ecv else 130
        hba1c = 7.0
        
    return pa_sys, pa_dia, ldl, hba1c

__all__ = [
    "calc_tfg_cg",
    "calc_imc",
    "get_estadio_erc",
    "calc_riesgo_cv_4_pasos",
    "get_metas_programa",
]
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
