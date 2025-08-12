"""
Cálculo de Tasa de Filtración Glomerular (TFG) y estadificación ERC.

Este módulo implementa los cálculos de aclaramiento de creatinina
usando la fórmula de Cockcroft-Gault, así como la clasificación 
por estadios de Enfermedad Renal Crónica (ERC).
"""

from __future__ import annotations
from typing import Dict, Optional, Union, List, Tuple, Any

# Para evitar importación circular, usamos TypeVar
from typing import TypeVar
Paciente = TypeVar('Paciente', bound=Any)

# Clasificación de estadios ERC
ESTADIOS_ERC = {
    (90, float('inf')): "E1",    # ≥90 ml/min: Normal o alto
    (60, 90): "E2",              # 60-89 ml/min: Levemente disminuido
    (45, 60): "E3A",             # 45-59 ml/min: Leve a moderado
    (30, 45): "E3B",             # 30-44 ml/min: Moderado a severo
    (15, 30): "E4",              # 15-29 ml/min: Severamente disminuido
    (0, 15): "E5",               # <15 ml/min: Fallo renal
}

# Mensajes explicativos por estadio
MENSAJES_ERC = {
    "E1": "Función renal normal o alta",
    "E2": "Disminución leve de la función renal",
    "E3A": "Disminución leve a moderada de la función renal",
    "E3B": "Disminución moderada a severa de la función renal",
    "E4": "Disminución severa de la función renal",
    "E5": "Fallo renal",
}

class PacienteData:
    """Clase para datos mínimos de paciente para cálculos TFG."""
    
    def __init__(
        self, 
        edad: int, 
        peso_kg: float, 
        sexo: str, 
        creatinina_mg_dl: Optional[float] = None
    ):
        """
        Inicializa datos para cálculo de TFG.
        
        Args:
            edad: Edad del paciente en años
            peso_kg: Peso en kilogramos
            sexo: Sexo biológico ('M' o 'F')
            creatinina_mg_dl: Valor de creatinina en mg/dL (opcional)
        """
        self.edad = edad
        self.peso_kg = peso_kg
        self.sexo = sexo.upper()
        self.creatinina_mg_dl = creatinina_mg_dl


def crcl_cockcroft_gault(
    paciente: Union[PacienteData, 'Paciente'], 
    creatinina_mg_dl: Optional[float] = None
) -> Optional[float]:
    """
    Calcula el aclaramiento de creatinina usando la fórmula de Cockcroft-Gault.
    
    Fórmula: ((140 - edad) * peso(kg) * (0.85 si mujer)) / (72 * Cr)
    
    Args:
        paciente: Objeto paciente con datos necesarios
        creatinina_mg_dl: Valor de creatinina en mg/dL (opcional)
        
    Returns:
        Aclaramiento de creatinina en ml/min o None si faltan datos
    """
    # Verificar datos necesarios
    if getattr(paciente, 'peso_kg', None) is None:
        return None
    
    # Usar creatinina proporcionada o buscar en labs del paciente
    cr_valor = creatinina_mg_dl
    if cr_valor is None:
        cr_valor = getattr(paciente, 'creatinina_mg_dl', None)
        
    # Si aún es None, intentar buscar en labs si es paciente completo
    if cr_valor is None and hasattr(paciente, 'labs'):
        labs = [l for l in paciente.labs if l.nombre == "CREATININA EN SUERO U OTROS"]
        if not labs:
            return None
        cr_valor = sorted(labs, key=lambda x: x.fecha)[-1].valor
    
    # Validación final
    if cr_valor is None or cr_valor <= 0:
        return None
        
    # Aplicar fórmula
    factor_sexo = 0.85 if paciente.sexo == "F" else 1.0
    crcl = ((140 - paciente.edad) * paciente.peso_kg * factor_sexo) / (72 * cr_valor)
    
    return round(crcl, 2)


def get_estadio_erc(tfg: float) -> str:
    """
    Determina el estadio de ERC basado en la TFG.
    
    Args:
        tfg: Tasa de filtración glomerular en ml/min
        
    Returns:
        Estadio ERC como string (E1-E5)
    """
    for rango, estadio in ESTADIOS_ERC.items():
        min_val, max_val = rango
        if min_val <= tfg < max_val:
            return estadio
    return "E5"  # Default para valores extremadamente bajos


def get_mensaje_erc(estadio: str) -> str:
    """
    Obtiene mensaje explicativo para un estadio ERC.
    
    Args:
        estadio: Estadio ERC (E1-E5)
        
    Returns:
        Mensaje explicativo
    """
    return MENSAJES_ERC.get(estadio, "Estadio no identificado")


def calcular_tfg_completo(paciente: Union[PacienteData, 'Paciente']) -> Dict:
    """
    Realiza cálculo completo de TFG y estadiaje ERC.
    
    Args:
        paciente: Objeto paciente con datos necesarios
        
    Returns:
        Diccionario con resultados completos (tfg, estadio, mensaje)
    """
    tfg = crcl_cockcroft_gault(paciente)
    
    if tfg is None:
        return {
            "tfg": None,
            "estadio": None,
            "mensaje": "No se puede calcular la TFG. Verifique los datos.",
            "datos_completos": False
        }
        
    estadio = get_estadio_erc(tfg)
    mensaje = get_mensaje_erc(estadio)
    
    return {
        "tfg": tfg,
        "estadio": estadio,
        "mensaje": mensaje,
        "datos_completos": True
    }


__all__ = [
    "crcl_cockcroft_gault", 
    "get_estadio_erc", 
    "get_mensaje_erc",
    "calcular_tfg_completo",
    "PacienteData",
    "ESTADIOS_ERC",
    "MENSAJES_ERC"
]
