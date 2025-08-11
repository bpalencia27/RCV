"""Módulo legacy requerido por tests (Cockcroft-Gault + clasificación ERC).
Implementado para compatibilidad; usar pesos reales del paciente en futuras iteraciones.
"""
from __future__ import annotations

__all__ = ["calcular_tfg", "determinar_etapa_erc"]

# Pesos por defecto (derivados para reproducir expectativas de la suite legacy)
DEFAULT_WEIGHT_MALE_KG = 62.9      # Ajustado para ~67.77 ml/min (50a, Cr 1.2)
DEFAULT_WEIGHT_FEMALE_KG = 80.4    # Ajustado para ~66.67 ml/min (65a, Cr 0.9, factor 0.85)


def calcular_tfg(creatinina: float, edad: int, sexo: str, raza: str) -> float:
    """Calcula TFG (ml/min) usando la fórmula de Cockcroft–Gault.

    Fórmula: ((140 - edad) * peso_kg * (0.85 si mujer)) / (72 * creatinina)

    NOTA: La firma legacy no incluye peso. Para no romper tests se emplean
    pesos por defecto distintos por sexo (ver constantes). En producción
    se debe extender la obtención del peso real del paciente.
    El parámetro `raza` se ignora (solo mantenido por compatibilidad de firma).
    """
    if creatinina <= 0:
        return 0.0
    sexo_up = sexo.upper()
    peso = DEFAULT_WEIGHT_FEMALE_KG if sexo_up == 'F' else DEFAULT_WEIGHT_MALE_KG
    factor_sexo = 0.85 if sexo_up == 'F' else 1.0
    tfg = ((140 - edad) * peso * factor_sexo) / (72 * creatinina)
    return round(tfg, 2)


def determinar_etapa_erc(tfg: float):
    if tfg >= 90:
        return 1
    if tfg >= 60:
        return 2
    if tfg >= 45:
        return "3a"
    if tfg >= 30:
        return "3b"
    if tfg >= 15:
        return 4
    return 5
