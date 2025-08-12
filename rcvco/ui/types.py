"""Tipos de datos y constantes compartidas en UI."""
from __future__ import annotations
from enum import Enum

class EstadioERC(str, Enum):
    """Estadios ERC para tipado seguro."""
    E1 = "E1"    # TFG ≥90
    E2 = "E2"    # TFG 60-89
    E3A = "E3A"  # TFG 45-59 
    E3B = "E3B"  # TFG 30-44
    E4 = "E4"    # TFG 15-29
    E5 = "E5"    # TFG <15

class RiesgoCV(str, Enum):
    """Categorías riesgo CV (4 Pasos)."""
    MUY_ALTO = "Muy alto"  
    ALTO = "Alto"
    MODERADO = "Moderado"
    BAJO = "Bajo"

class Programa(str, Enum):
    """Programas prioritarios."""
    ERC = "ERC"  # prioridad 1
    DM = "DM"    # prioridad 2 
    HTA = "HTA"  # prioridad 3

class Sexo(str, Enum):
    """Sexo biológico (para Cockcroft-Gault)."""
    M = "M"  # masculino
    F = "F"  # femenino

__all__ = ["EstadioERC", "RiesgoCV", "Programa", "Sexo"]
