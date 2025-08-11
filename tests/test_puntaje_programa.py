from datetime import date
from rcvco.domain.models import Paciente, LabResult
from rcvco.domain.scoring import calcula_puntaje


def test_puntaje_basico_erc_sin_dm():
    p = Paciente(pseudo_id="erc", sexo="M", edad=68, peso_kg=70, labs=[
        LabResult(nombre="CREATININA EN SUERO U OTROS", valor=2.0, unidad="mg/dL", fecha=date(2025,8,10)),
        LabResult(nombre="COLESTEROL LDL", valor=135, unidad="mg/dL", fecha=date(2025,8,10)),
        LabResult(nombre="PRESION ARTERIAL SISTOLICA", valor=148, unidad="mmHg", fecha=date(2025,8,10)),
    ])
    s = calcula_puntaje(p)
    assert s >= 4
