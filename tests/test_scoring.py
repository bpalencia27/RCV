from datetime import date
from rcvco.domain.models import Paciente, LabResult
from rcvco.domain.scoring import calcula_puntaje


def test_calcula_puntaje_componentes():
    p = Paciente(
        pseudo_id="s1",
        sexo="F",
        edad=70,
        peso_kg=70,
        labs=[
            LabResult(nombre="COLESTEROL LDL", valor=165, unidad="mg/dL", fecha=date(2025, 1, 1)),
            LabResult(
                nombre="HEMOGLOBINA GLICOSILADA (HBA1C)",
                valor=8.1,
                unidad="%",
                fecha=date(2025, 2, 1),
            ),
            LabResult(
                nombre="PRESION ARTERIAL SISTOLICA",
                valor=162,
                unidad="mmHg",
                fecha=date(2025, 3, 1),
            ),
            LabResult(
                nombre="CREATININA EN SUERO U OTROS",
                valor=1.4,
                unidad="mg/dL",
                fecha=date(2025, 4, 1),
            ),
        ],
    )
    s = calcula_puntaje(p)
    # Edad 2 + LDL 2 + HbA1c 2 + PAS 2 + Creatinina 1 = 9
    assert s == 9
