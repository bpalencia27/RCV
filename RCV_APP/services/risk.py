"""
Evaluación de riesgo cardiovascular.

Este módulo implementa la clasificación de riesgo CV usando
el protocolo de 4 pasos, cálculo de puntaje y estimación ASCVD.
"""

from __future__ import annotations
from typing import Dict, Optional, Union, List, Tuple, Any, TypeVar

# Para evitar importación circular, usamos TypeVar
Paciente = TypeVar('Paciente', bound=Any)

# Categorías de riesgo
RIESGO_CATEGORIAS = [
    (6, "Muy Alto"),
    (4, "Alto"),
    (2, "Moderado"),
    (0, "Bajo"),
]

# Explicaciones por categoría
RIESGO_EXPLICACIONES = {
    "Muy Alto": "Paciente con riesgo cardiovascular muy alto que requiere intervención intensiva.",
    "Alto": "Paciente con riesgo cardiovascular alto que requiere seguimiento estrecho.",
    "Moderado": "Paciente con riesgo cardiovascular moderado que requiere vigilancia periódica.",
    "Bajo": "Paciente con riesgo cardiovascular bajo que puede seguir controles habituales.",
}


class LabValor:
    """Representación simple de un resultado de laboratorio."""
    
    def __init__(self, nombre: str, valor: float, fecha=None):
        """
        Inicializa un resultado de laboratorio.
        
        Args:
            nombre: Nombre del examen
            valor: Valor numérico del resultado
            fecha: Fecha del examen (opcional)
        """
        self.nombre = nombre
        self.valor = valor
        self.fecha = fecha


class PacienteRiesgo:
    """Clase para datos mínimos de paciente para evaluación de riesgo."""
    
    def __init__(
        self,
        edad: int,
        sexo: str,
        labs: Optional[List[LabValor]] = None,
        estadio_erc: Optional[str] = None,
        has_dm: bool = False,
        has_hta: bool = False
    ):
        """
        Inicializa datos para evaluación de riesgo.
        
        Args:
            edad: Edad del paciente en años
            sexo: Sexo biológico ('M' o 'F')
            labs: Lista de resultados de laboratorio
            estadio_erc: Estadio de enfermedad renal crónica
            has_dm: Si tiene diagnóstico de diabetes
            has_hta: Si tiene diagnóstico de hipertensión
        """
        self.edad = edad
        self.sexo = sexo.upper()
        self.labs = labs or []
        self.estadio_erc = estadio_erc
        self.has_dm = has_dm
        self.has_hta = has_hta


def _ultimo_lab(labs: List[LabValor], nombre: str) -> Optional[LabValor]:
    """
    Obtiene el último resultado de un tipo de laboratorio.
    
    Args:
        labs: Lista de resultados de laboratorio
        nombre: Nombre del examen a buscar
        
    Returns:
        El resultado más reciente o None si no existe
    """
    filtrados = [l for l in labs if l.nombre == nombre]
    if not filtrados:
        return None
        
    # Si hay fecha, ordenar por fecha
    if hasattr(filtrados[0], 'fecha') and filtrados[0].fecha is not None:
        return sorted(filtrados, key=lambda x: x.fecha)[-1]
    
    # Si no hay fecha, devolver el primero
    return filtrados[0]


def calcula_puntaje(paciente: Union[PacienteRiesgo, Paciente]) -> int:
    """
    Calcula el puntaje de riesgo cardiovascular.
    
    Puntaje simplificado:
    - Edad: >= 65 -> +2
    - LDL >= 160 -> +2, 130-159 -> +1
    - HbA1c >= 8 -> +2, 7-7.9 -> +1
    - PAS >= 140 -> +1, >=160 -> +2
    - Creatinina >= 1.3 -> +1
    - ERC estadio >= 3 -> +1
    - Diagnóstico DM -> +1
    - Diagnóstico HTA -> +1
    
    Args:
        paciente: Objeto paciente con datos necesarios
        
    Returns:
        Puntaje numérico de riesgo (0-10)
    """
    score = 0
    
    # Puntos por edad
    if paciente.edad >= 65:
        score += 2
        
    # Buscar labs relevantes
    labs = getattr(paciente, 'labs', [])
    
    # LDL
    ldl = _ultimo_lab(labs, "COLESTEROL LDL")
    if ldl:
        if ldl.valor >= 160:
            score += 2
        elif ldl.valor >= 130:
            score += 1
            
    # HbA1c
    hba1c = _ultimo_lab(labs, "HEMOGLOBINA GLICOSILADA (HBA1C)")
    if hba1c:
        if hba1c.valor >= 8:
            score += 2
        elif hba1c.valor >= 7:
            score += 1
            
    # Presión arterial sistólica
    pas = _ultimo_lab(labs, "PRESION ARTERIAL SISTOLICA")
    if pas:
        if pas.valor >= 160:
            score += 2
        elif pas.valor >= 140:
            score += 1
            
    # Creatinina
    crea = _ultimo_lab(labs, "CREATININA EN SUERO U OTROS")
    if crea and crea.valor >= 1.3:
        score += 1
        
    # Estadio ERC
    estadio = getattr(paciente, 'estadio_erc', None)
    if estadio and estadio in ["E3A", "E3B", "E4", "E5"]:
        score += 1
        
    # Diagnósticos
    if getattr(paciente, 'has_dm', False):
        score += 1
        
    if getattr(paciente, 'has_hta', False):
        score += 1
        
    return score


def clasificar_riesgo_cv_4_pasos(paciente: Union[PacienteRiesgo, Paciente]) -> str:
    """
    Clasifica el riesgo cardiovascular según protocolo de 4 pasos.
    
    Args:
        paciente: Objeto paciente con datos necesarios
        
    Returns:
        Categoría de riesgo ("Muy Alto", "Alto", "Moderado", "Bajo")
    """
    score = calcula_puntaje(paciente)
    
    for umbral, nombre in RIESGO_CATEGORIAS:
        if score >= umbral:
            return nombre
            
    return "Bajo"  # Default


def ascvd_ajustado(paciente: Union[PacienteRiesgo, Paciente]) -> float:
    """
    Calcula el riesgo ASCVD a 10 años ajustado.
    
    Args:
        paciente: Objeto paciente con datos necesarios
        
    Returns:
        Porcentaje de riesgo ASCVD (0-100%)
    """
    score = calcula_puntaje(paciente)
    
    # Modelo simplificado: 5% base + 2% por punto de score
    riesgo = 5 + score * 2.0
    
    # Limitar a 100%
    return min(100.0, riesgo)


def evaluacion_completa(paciente: Union[PacienteRiesgo, Paciente]) -> Dict:
    """
    Realiza evaluación completa de riesgo cardiovascular.
    
    Args:
        paciente: Objeto paciente con datos necesarios
        
    Returns:
        Diccionario con resultados completos
    """
    score = calcula_puntaje(paciente)
    categoria = clasificar_riesgo_cv_4_pasos(paciente)
    ascvd = ascvd_ajustado(paciente)
    explicacion = RIESGO_EXPLICACIONES.get(categoria, "")
    
    return {
        "score": score,
        "categoria": categoria,
        "ascvd": ascvd,
        "explicacion": explicacion,
        "datos_completos": True
    }


__all__ = [
    "calcula_puntaje",
    "clasificar_riesgo_cv_4_pasos",
    "ascvd_ajustado",
    "evaluacion_completa",
    "PacienteRiesgo",
    "LabValor",
    "RIESGO_CATEGORIAS",
    "RIESGO_EXPLICACIONES"
]
