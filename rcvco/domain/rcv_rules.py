from __future__ import annotations
from datetime import date, timedelta
from typing import List, Optional, Tuple
from .models import AgendaItem

UNIFICACION_DIAS = 14
_RANGO = lambda x: (x, x)

INTERVALOS = {
    "PARCIAL DE ORINA": {"E1": _RANGO(180), "E2": _RANGO(180), "E3A": _RANGO(180), "E3B": _RANGO(180), "E4": _RANGO(120)},
    "CREATININA EN SUERO U OTROS": {"E1": _RANGO(180), "E2": _RANGO(180), "E3A": (90, 121), "E3B": (90, 121), "E4": (60, 93)},
    "GLUCOSA EN AYUNAS": {"E1": _RANGO(180), "E2": _RANGO(180), "E3A": _RANGO(180), "E3B": _RANGO(180), "E4": _RANGO(60)},
    "COLESTEROL TOTAL": {"E1": _RANGO(180), "E2": _RANGO(180), "E3A": _RANGO(180), "E3B": _RANGO(180), "E4": _RANGO(120)},
    "COLESTEROL LDL": {"E1": _RANGO(180), "E2": _RANGO(180), "E3A": _RANGO(180), "E3B": _RANGO(180), "E4": _RANGO(180)},
    "TRIGLICERIDOS": {"E1": _RANGO(180), "E2": _RANGO(180), "E3A": _RANGO(180), "E3B": _RANGO(180), "E4": _RANGO(120)},
    "HEMOGLOBINA GLICOSILADA (HBA1C)": {"E1": _RANGO(180), "E2": _RANGO(180), "E3A": _RANGO(180), "E3B": _RANGO(180), "E4": _RANGO(120)},
    "RAC": {"E1": _RANGO(180), "E2": _RANGO(180), "E3A": _RANGO(180), "E3B": _RANGO(180), "E4": _RANGO(180)},
    "HEMOGLOBINA": {"E1": _RANGO(365), "E2": _RANGO(365), "E3A": _RANGO(365), "E3B": _RANGO(365), "E4": _RANGO(180)},
    "HEMATOCRITO": {"E1": _RANGO(365), "E2": _RANGO(365), "E3A": _RANGO(365), "E3B": _RANGO(365), "E4": _RANGO(180)},
    "PTH": {"E1": None, "E2": None, "E3A": _RANGO(365), "E3B": _RANGO(365), "E4": _RANGO(180)},
    "ALBUMINA": {"E1": None, "E2": None, "E3A": None, "E3B": _RANGO(365), "E4": _RANGO(365)},
    "FOSFORO": {"E1": None, "E2": None, "E3A": None, "E3B": _RANGO(365), "E4": _RANGO(365)},
    "DEPURACION CREATININA ORINA 24H": {"E1": _RANGO(365), "E2": _RANGO(180), "E3A": _RANGO(180), "E3B": _RANGO(180), "E4": _RANGO(90)},
}
EXAM_ORDER = list(INTERVALOS.keys())

def _normalizar_estadio(estadio: str) -> str:
    e = estadio.upper().strip()
    return e if e in {"E1","E2","E3A","E3B","E4"} else "E1"

def _calcular_fecha(fecha_base: date, rango: Tuple[int, int], hoy: date) -> date:
    d_min, d_max = rango
    fecha_min = fecha_base + timedelta(days=d_min)
    if fecha_min < hoy:
        return fecha_base + timedelta(days=d_max)
    return fecha_min

def generar_agenda_avanzada(fecha_base: date, estadio: str, tiene_dm: bool, ldl_val: Optional[float] = None, hoy: Optional[date] = None) -> List[AgendaItem]:
    hoy = hoy or fecha_base
    estadio_n = _normalizar_estadio(estadio)
    agenda: List[AgendaItem] = []
    for examen in EXAM_ORDER:
        if examen == "HEMOGLOBINA GLICOSILADA (HBA1C)" and not tiene_dm:
            continue
        conf = INTERVALOS[examen][estadio_n]
        if conf is None:
            continue
        fecha_prog = _calcular_fecha(fecha_base, conf, hoy)
        agenda.append(AgendaItem(
            examen=examen,
            fecha_programada=fecha_prog,
            motivo=f"Seguimiento {examen.lower()}",
            revision_fecha=fecha_prog + timedelta(days=7),
        ))
    agenda.sort(key=lambda a: a.fecha_programada)
    i = 0
    while i < len(agenda):
        grupo = [agenda[i]]
        j = i + 1
        while j < len(agenda) and (agenda[j].fecha_programada - agenda[i].fecha_programada).days <= UNIFICACION_DIAS:
            grupo.append(agenda[j])
            j += 1
        if len(grupo) > 1:
            fecha_ref = grupo[0].fecha_programada
            for g in grupo:
                g.fecha_programada = fecha_ref
                g.revision_fecha = fecha_ref + timedelta(days=7)
        i = j
    return agenda

__all__ = ["generar_agenda_avanzada"]
