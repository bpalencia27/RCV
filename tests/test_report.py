from datetime import date
from rcvco.domain.models import Paciente, LabResult, ResumenRiesgo, AgendaItem
from rcvco.domain.report import generar_informe


def test_generar_informe_contiene_fechas():
    p = Paciente(pseudo_id="rep1", sexo="M", edad=60, peso_kg=80, labs=[])
    resumen = ResumenRiesgo(
        riesgo_categoria="Moderado",
        puntaje=3,
        ascvd=11.5,
        aclaramiento_creatinina=70.2,
        agenda=[
            AgendaItem(
                examen="COLESTEROL LDL",
                fecha_programada=date(2025, 7, 1),
                motivo="Seguimiento dislipidemia",
                revision_fecha=date(2025, 7, 8),
            )
        ],
    )
    informe = generar_informe(p, resumen)
    assert "COLESTEROL LDL" in informe.texto
    assert "Revisión: 2025-07-08" in informe.texto
