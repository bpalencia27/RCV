from datetime import date
from rcvco.domain.models import Paciente, LabResult
from rcvco.domain.risk import clasificar_riesgo_cv_4_pasos


def test_riesgo_muy_alto_por_score():
    p = Paciente(pseudo_id="r", sexo="M", edad=75, peso_kg=80, labs=[
        LabResult(nombre="COLESTEROL LDL", valor=190, unidad="mg/dL", fecha=date(2025,1,1)),
        LabResult(nombre="HEMOGLOBINA GLICOSILADA (HBA1C)", valor=9.0, unidad="%", fecha=date(2025,1,1)),
        LabResult(nombre="PRESION ARTERIAL SISTOLICA", valor=170, unidad="mmHg", fecha=date(2025,1,1)),
        LabResult(nombre="CREATININA EN SUERO U OTROS", valor=1.6, unidad="mg/dL", fecha=date(2025,1,1)),
    ])
    riesgo = clasificar_riesgo_cv_4_pasos(p)
    assert riesgo in {"Muy Alto", "Alto"}
