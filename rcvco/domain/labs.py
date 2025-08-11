from __future__ import annotations
from datetime import date, timedelta
from typing import List, Iterable
from .models import Paciente, AgendaItem, LabResult
from .rcv_rules import generar_agenda_avanzada

# Reglas simplificadas X–Y (placeholder):
# - Creatinina: cada 90 días
# - HbA1c: si valor >=7 -> 90 días, si <7 -> 180 días
# - LDL: anual, pero si LDL >=130 -> 90 días
# Unificación: si dos exámenes caen en ventana de 14 días se mueven al mismo día (más temprano)
# Revisión +7: se agrega fecha revision_fecha = fecha_programada + 7 días

WINDOW_UNIFICACION_DIAS = 14

DEF_CREAS_INTERVAL = 90
DEF_LDL_INTERVAL = 365
DEF_LDL_ALTO_INTERVAL = 90
DEF_HBA1C_INTERVAL_BUENO = 180
DEF_HBA1C_INTERVAL_ALTO = 90


def _ultimo(labs: Iterable[LabResult], nombre: str):
    filtrados = [l for l in labs if l.nombre == nombre]
    return max(filtrados, key=lambda x: x.fecha) if filtrados else None


def _proxima_fecha(base: date, dias: int) -> date:
    return base + timedelta(days=dias)


def agenda_labs(paciente: Paciente, hoy: date | None = None) -> List[AgendaItem]:
    hoy = hoy or date.today()
    items: List[AgendaItem] = []

    # Creatinina sérica precisa la etiqueta exacta
    creat = _ultimo(paciente.labs, "CREATININA EN SUERO U OTROS")
    if creat:
        items.append(
            AgendaItem(
                examen="CREATININA EN SUERO U OTROS",
                fecha_programada=_proxima_fecha(creat.fecha, DEF_CREAS_INTERVAL),
                motivo="Seguimiento función renal",
                revision_fecha=_proxima_fecha(creat.fecha, DEF_CREAS_INTERVAL + 7),
            )
        )

    hba1c = _ultimo(paciente.labs, "HEMOGLOBINA GLICOSILADA (HBA1C)")
    if hba1c:
        intervalo = DEF_HBA1C_INTERVAL_ALTO if hba1c.valor >= 7 else DEF_HBA1C_INTERVAL_BUENO
        items.append(
            AgendaItem(
                examen="HEMOGLOBINA GLICOSILADA (HBA1C)",
                fecha_programada=_proxima_fecha(hba1c.fecha, intervalo),
                motivo="Control glucémico",
                revision_fecha=_proxima_fecha(hba1c.fecha, intervalo + 7),
            )
        )

    ldl = _ultimo(paciente.labs, "COLESTEROL LDL")
    if ldl:
        intervalo = DEF_LDL_ALTO_INTERVAL if ldl.valor >= 130 else DEF_LDL_INTERVAL
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
            ).days <= WINDOW_UNIFICACION_DIAS:
                # Unificar al más temprano
                fecha_base = items[i].fecha_programada
                items[j].fecha_programada = fecha_base
                items[j].revision_fecha = fecha_base + timedelta(days=7)

    return items


def agenda_labs_v2(paciente: Paciente, estadio: str = "E1", tiene_dm: bool = False, hoy: date | None = None) -> List[AgendaItem]:
    """Agenda avanzada usando reglas v2.0 (wrapper)."""
    hoy = hoy or date.today()
    base = max((l.fecha for l in paciente.labs), default=hoy)
    return generar_agenda_avanzada(base, estadio=estadio, tiene_dm=tiene_dm, hoy=hoy)

__all__ = ["agenda_labs", "agenda_labs_v2"]
