from datetime import date
from rcvco.domain.models import Paciente, LabResult
from rcvco.domain.risk import clasificar_riesgo_cv_4_pasos
from rcvco.domain.scoring import calcula_puntaje


def test_clasificar_riesgo_muy_alto():
    p = Paciente(
        pseudo_id="r1",
        sexo="M",
        edad=70,
        peso_kg=80,
        labs=[
            LabResult(nombre="COLESTEROL LDL", valor=190, unidad="mg/dL", fecha=date(2025, 1, 1)),
            LabResult(
                nombre="HEMOGLOBINA GLICOSILADA (HBA1C)",
                valor=9.0,
                unidad="%",
                fecha=date(2025, 2, 1),
            ),
            LabResult(
                nombre="PRESION ARTERIAL SISTOLICA",
                valor=170,
                unidad="mmHg",
                fecha=date(2025, 3, 1),
            ),
            LabResult(
                nombre="CREATININA EN SUERO U OTROS",
                valor=1.5,
                unidad="mg/dL",
                fecha=date(2025, 4, 1),
            ),
        ],
    )
    riesgo = clasificar_riesgo_cv_4_pasos(p)
    score = calcula_puntaje(p)
    assert score >= 6
    assert riesgo == "Muy Alto"
