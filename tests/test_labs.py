from datetime import date
from rcvco.domain.models import Paciente, LabResult
from rcvco.domain.labs import agenda_labs


def _paciente_base():
    return Paciente(
        pseudo_id="t1",
        sexo="M",
        edad=60,
        peso_kg=80,
        labs=[
            LabResult(
                nombre="CREATININA EN SUERO U OTROS",
                valor=1.2,
                unidad="mg/dL",
                fecha=date(2025, 1, 1),
            ),
            LabResult(
                nombre="HEMOGLOBINA GLICOSILADA (HBA1C)",
                valor=6.8,
                unidad="%",
                fecha=date(2025, 2, 1),
            ),
            LabResult(nombre="COLESTEROL LDL", valor=120, unidad="mg/dL", fecha=date(2025, 3, 1)),
        ],
    )


def test_agenda_basica_intervalos():
    p = _paciente_base()
    ag = agenda_labs(p, hoy=date(2025, 4, 1))
    nombres = {i.examen for i in ag}
    assert "CREATININA EN SUERO U OTROS" in nombres
    assert "HEMOGLOBINA GLICOSILADA (HBA1C)" in nombres
    assert "COLESTEROL LDL" in nombres
    # Verificar revisión +7
    for item in ag:
        assert (item.revision_fecha - item.fecha_programada).days == 7


def test_unificacion_ventana():
    p = _paciente_base()
    # Ajustar fechas para forzar proximidad
    p.labs.append(
        LabResult(nombre="COLESTEROL LDL", valor=150, unidad="mg/dL", fecha=date(2025, 3, 10))
    )
    ag = agenda_labs(p)
    # Debe haber un único LDL programado
    ldls = [i for i in ag if i.examen == "COLESTEROL LDL"]
    assert len(ldls) == 1
