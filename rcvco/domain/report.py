from __future__ import annotations
from datetime import datetime
from .models import Paciente, Informe, ResumenRiesgo, AgendaItem


def generar_informe(paciente: Paciente, resumen: ResumenRiesgo) -> Informe:
    lineas: list[str] = []
    lineas.append("Evaluación de riesgo cardiovascular y seguimiento.")
    lineas.append(f"Categoría de riesgo: {resumen.riesgo_categoria} (puntaje {resumen.puntaje}).")
    if resumen.ascvd is not None:
        lineas.append(f"Riesgo estimado a 10 años: {resumen.ascvd:.1f}%.")
    if resumen.aclaramiento_creatinina is not None:
        lineas.append(
            f"Aclaramiento de creatinina estimado: {resumen.aclaramiento_creatinina} ml/min."
        )
    if resumen.agenda:
        lineas.append("Próximos laboratorios programados:")
        for a in resumen.agenda:
            lineas.append(
                f" - {a.examen}: {a.fecha_programada.isoformat()} (Revisión: {a.revision_fecha.isoformat()})"
            )
    texto = "\n".join(lineas)
    return Informe(generado_en=datetime.utcnow(), texto=texto)


__all__ = ["generar_informe"]
