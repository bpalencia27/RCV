"""
Laboratorios, cálculo de agenda y seguimiento.

Este módulo implementa las reglas clínicas de frecuencia de laboratorios
según el estadio de ERC y condiciones del paciente. Sigue la regla X-Y días
donde:
- X: Días para evaluar vencimiento (comparando fecha actual vs último lab)
- Y: Días para programar siguiente lab si está vencido

También maneja la unificación de labs que caen en fechas cercanas.
"""

from __future__ import annotations
from datetime import date, timedelta
from typing import List, Optional, Dict, Tuple, Any, TypeVar, Union
from dataclasses import dataclass

# Para evitar importación circular, usamos TypeVar
Paciente = TypeVar('Paciente', bound=Any)

# Configuración de unificación: si dos labs caen en un rango de 14 días, 
# se programan para la misma fecha (la del último)
UNIFICACION_DIAS = 14

# Mapeo de intervalos por estadio y lab (días)
# Formato: (días para evaluar vencimiento, días para programar si vencido)
# Si no hay rango, ambos valores son iguales
_RANGO = lambda x: (x, x)

INTERVALOS = {
    "PARCIAL DE ORINA": {
        "E1": _RANGO(180), "E2": _RANGO(180), 
        "E3A": _RANGO(180), "E3B": _RANGO(180), 
        "E4": _RANGO(120),
    },
    "CREATININA EN SUERO U OTROS": {
        "E1": _RANGO(180), "E2": _RANGO(180), 
        "E3A": (90, 121), "E3B": (90, 121), 
        "E4": (60, 93),
    },
    "GLICEMIA": {
        "E1": _RANGO(180), "E2": _RANGO(180), 
        "E3A": _RANGO(180), "E3B": _RANGO(180), 
        "E4": _RANGO(60),
    },
    "COLESTEROL TOTAL": {
        "E1": _RANGO(180), "E2": _RANGO(180), 
        "E3A": _RANGO(180), "E3B": _RANGO(180), 
        "E4": _RANGO(120),
    },
    "COLESTEROL LDL": {
        "E1": _RANGO(180), "E2": _RANGO(180), 
        "E3A": _RANGO(180), "E3B": _RANGO(180), 
        "E4": _RANGO(180),
    },
    "TRIGLICERIDOS": {
        "E1": _RANGO(180), "E2": _RANGO(180), 
        "E3A": _RANGO(180), "E3B": _RANGO(180), 
        "E4": _RANGO(120),
    },
    "HEMOGLOBINA GLICOSILADA (HBA1C)": {
        "E1": _RANGO(180), "E2": _RANGO(180), 
        "E3A": _RANGO(180), "E3B": _RANGO(180), 
        "E4": _RANGO(120),
    },
    "MICROALBUMINURIA/RELACION (RAC/ACR)": {
        "E1": _RANGO(180), "E2": _RANGO(180), 
        "E3A": _RANGO(180), "E3B": _RANGO(180), 
        "E4": _RANGO(180),
    },
    "HEMOGLOBINA SERICA": {
        "E1": _RANGO(365), "E2": _RANGO(365), 
        "E3A": _RANGO(365), "E3B": _RANGO(365), 
        "E4": _RANGO(180),
    },
    "HEMATOCRITO": {
        "E1": _RANGO(365), "E2": _RANGO(365), 
        "E3A": _RANGO(365), "E3B": _RANGO(365), 
        "E4": _RANGO(180),
    },
    "PTH": {
        "E1": None, "E2": None, 
        "E3A": _RANGO(365), "E3B": _RANGO(365), 
        "E4": _RANGO(180),
    },
    "ALBUMINA": {
        "E1": None, "E2": None, 
        "E3A": None, "E3B": _RANGO(365), 
        "E4": _RANGO(365),
    },
    "FOSFORO SERICO": {
        "E1": None, "E2": None, 
        "E3A": None, "E3B": _RANGO(365), 
        "E4": _RANGO(365),
    },
    "DEPURACION CREATININA 24H ORINA": {
        "E1": _RANGO(365), "E2": _RANGO(180), 
        "E3A": _RANGO(180), "E3B": _RANGO(180), 
        "E4": _RANGO(90),
    },
}

# Orden de presentación de exámenes en informe
EXAM_ORDER = list(INTERVALOS.keys())


@dataclass
class LabResult:
    """Resultado de laboratorio simplificado."""
    nombre: str
    valor: float
    fecha: date
    unidad: str = ""


@dataclass
class AgendaItem:
    """Ítem de agenda de laboratorios."""
    examen: str
    fecha_programada: date
    motivo: str
    revision_fecha: date


class PacienteLabs:
    """Clase para datos mínimos de paciente para agenda de labs."""
    
    def __init__(
        self,
        labs: List[LabResult] = None,
        estadio_erc: str = "E1",
        tiene_dm: bool = False
    ):
        """
        Inicializa datos para cálculo de agenda.
        
        Args:
            labs: Lista de resultados de laboratorio
            estadio_erc: Estadio ERC (E1-E5)
            tiene_dm: Si tiene diagnóstico de diabetes
        """
        self.labs = labs or []
        self.estadio_erc = estadio_erc
        self.tiene_dm = tiene_dm


def _ultimo(labs: List[LabResult], nombre: str) -> Optional[LabResult]:
    """
    Obtiene el último resultado de lab por nombre.
    
    Args:
        labs: Lista de resultados de laboratorio
        nombre: Nombre exacto del lab a buscar
        
    Returns:
        El resultado más reciente o None si no hay resultados
    """
    filtrados = [l for l in labs if l.nombre == nombre]
    if not filtrados:
        return None
    return sorted(filtrados, key=lambda x: x.fecha)[-1]


def _calcular_fecha(fecha_base: date, rango: Tuple[int, int], hoy: date) -> date:
    """
    Calcula la fecha del próximo lab según regla X-Y.
    
    Args:
        fecha_base: Fecha del último lab o fecha actual si no hay
        rango: Tupla (X, Y) de días para evaluar vencimiento y programar
        hoy: Fecha actual para comparación
        
    Returns:
        Fecha calculada para el próximo lab
    """
    dias_evaluar, dias_programar = rango
    
    # Calcular fecha límite para evaluación de vencimiento
    fecha_limite = fecha_base + timedelta(days=dias_evaluar)
    
    # Si ya venció, programar con Y días desde hoy
    if fecha_limite <= hoy:
        return hoy + timedelta(days=dias_programar)
    
    # Si no venció, programar con X días desde la fecha base
    return fecha_base + timedelta(days=dias_evaluar)


def _normalizar_estadio(estadio: str) -> str:
    """
    Normaliza el formato del estadio ERC.
    
    Args:
        estadio: Estadio en cualquier formato (1, E1, etc.)
        
    Returns:
        Estadio normalizado (E1, E2, E3A, E3B, E4)
    """
    if not estadio:
        return "E1"  # Default
    
    estadio = str(estadio).upper()
    if not estadio.startswith("E"):
        estadio = "E" + estadio
    
    return estadio


def _proxima_fecha(base: date, dias: int) -> date:
    """
    Calcula fecha futura a partir de base y días.
    
    Args:
        base: Fecha base para el cálculo
        dias: Días a sumar
        
    Returns:
        Nueva fecha calculada
    """
    return base + timedelta(days=dias)


def agenda_labs_simplificada(paciente: PacienteLabs, hoy: Optional[date] = None) -> List[AgendaItem]:
    """
    Genera agenda simplificada de laboratorios.
    
    Implementa la lógica simplificada para creatinina, HbA1c y LDL:
    - Creatinina: cada 90 días
    - HbA1c: si valor >=7 -> 90 días, si <7 -> 180 días
    - LDL: anual, pero si LDL >=130 -> 90 días
    
    Args:
        paciente: Datos del paciente incluyendo labs previos
        hoy: Fecha de referencia (default: date.today())
        
    Returns:
        Lista de items de agenda con examen, fecha y motivo
    """
    hoy = hoy or date.today()
    items: List[AgendaItem] = []

    # Creatinina sérica
    creat = _ultimo(paciente.labs, "CREATININA EN SUERO U OTROS")
    if creat:
        items.append(
            AgendaItem(
                examen="CREATININA EN SUERO U OTROS",
                fecha_programada=_proxima_fecha(creat.fecha, 90),
                motivo="Seguimiento función renal",
                revision_fecha=_proxima_fecha(creat.fecha, 90 + 7),
            )
        )

    # HbA1c (solo si tiene diabetes)
    if paciente.tiene_dm:
        hba1c = _ultimo(paciente.labs, "HEMOGLOBINA GLICOSILADA (HBA1C)")
        if hba1c:
            intervalo = 90 if hba1c.valor >= 7 else 180
            items.append(
                AgendaItem(
                    examen="HEMOGLOBINA GLICOSILADA (HBA1C)",
                    fecha_programada=_proxima_fecha(hba1c.fecha, intervalo),
                    motivo="Control glucémico",
                    revision_fecha=_proxima_fecha(hba1c.fecha, intervalo + 7),
                )
            )

    # LDL
    ldl = _ultimo(paciente.labs, "COLESTEROL LDL")
    if ldl:
        intervalo = 90 if ldl.valor >= 130 else 365
        items.append(
            AgendaItem(
                examen="COLESTEROL LDL",
                fecha_programada=_proxima_fecha(ldl.fecha, intervalo),
                motivo="Seguimiento dislipidemia",
                revision_fecha=_proxima_fecha(ldl.fecha, intervalo + 7),
            )
        )

    # Unificación dentro de ventana: mover a la fecha mínima de los que colisionan
    items.sort(key=lambda i: i.fecha_programada)
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if (
                items[j].fecha_programada - items[i].fecha_programada
            ).days <= UNIFICACION_DIAS:
                # Unificar al más temprano
                fecha_base = items[i].fecha_programada
                items[j].fecha_programada = fecha_base
                items[j].revision_fecha = fecha_base + timedelta(days=7)

    return items


def agenda_labs_completa(
    paciente: Union[PacienteLabs, Paciente], 
    hoy: Optional[date] = None
) -> List[AgendaItem]:
    """
    Genera agenda avanzada usando reglas completas.
    
    Implementa todas las reglas del sistema X-Y para cada examen según estadio,
    con unificación de fechas cercanas y revisión a +7 días.
    
    Args:
        paciente: Datos del paciente incluyendo labs previos
        hoy: Fecha de referencia (default: date.today())
        
    Returns:
        Lista de items de agenda con examen, fecha y motivo
    """
    hoy = hoy or date.today()
    
    # Obtener atributos relevantes
    labs = getattr(paciente, 'labs', [])
    estadio = getattr(paciente, 'estadio_erc', 'E1')
    tiene_dm = getattr(paciente, 'tiene_dm', False)
    
    # Normalizar estadio
    estadio_n = _normalizar_estadio(estadio)
    
    # Usar la fecha del lab más reciente como base, o la fecha actual si no hay labs
    fecha_base = hoy
    if labs:
        fecha_base = max((l.fecha for l in labs), default=hoy)
    
    # Obtener LDL para casos especiales
    ldl_val = None
    ldl_lab = _ultimo(labs, "COLESTEROL LDL")
    if ldl_lab:
        ldl_val = ldl_lab.valor
    
    # Generar agenda
    agenda: List[AgendaItem] = []
    
    # Iterar por todos los exámenes en orden definido
    for examen in EXAM_ORDER:
        # Omitir HbA1c si no tiene DM
        if examen == "HEMOGLOBINA GLICOSILADA (HBA1C)" and not tiene_dm:
            continue
            
        # Obtener configuración para este examen y estadio
        conf = INTERVALOS.get(examen, {}).get(estadio_n)
        
        # Si la configuración es None, este examen no aplica para este estadio
        if conf is None:
            continue
            
        # Calcular fecha del próximo lab
        fecha_prog = _calcular_fecha(fecha_base, conf, hoy)
        
        # Crear item de agenda
        agenda.append(AgendaItem(
            examen=examen,
            fecha_programada=fecha_prog,
            motivo=f"Seguimiento {examen.lower()}",
            revision_fecha=fecha_prog + timedelta(days=7),
        ))
    
    # Ordenar por fecha programada
    agenda.sort(key=lambda a: a.fecha_programada)
    
    # Proceso de unificación de fechas cercanas
    i = 0
    while i < len(agenda):
        grupo = [agenda[i]]
        j = i + 1
        
        # Buscar labs que caen en ventana de unificación
        while j < len(agenda) and (agenda[j].fecha_programada - agenda[i].fecha_programada).days <= UNIFICACION_DIAS:
            grupo.append(agenda[j])
            j += 1
            
        # Si hay más de un lab en el grupo, unificar fechas
        if len(grupo) > 1:
            fecha_ref = grupo[0].fecha_programada
            for g in grupo:
                g.fecha_programada = fecha_ref
                g.revision_fecha = fecha_ref + timedelta(days=7)
                
        i = j
    
    return agenda


__all__ = [
    "agenda_labs_simplificada", 
    "agenda_labs_completa",
    "LabResult",
    "AgendaItem", 
    "PacienteLabs",
    "INTERVALOS",
    "EXAM_ORDER"
]
