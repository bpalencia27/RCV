from datetime import date
from rcvco.domain.models import Paciente, LabResult
from rcvco.domain.tfg import crcl_cockcroft_gault


def test_cg_hombre():
    p = Paciente(pseudo_id="h", sexo="M", edad=65, peso_kg=80, labs=[
        LabResult(nombre="CREATININA EN SUERO U OTROS", valor=1.2, unidad="mg/dL", fecha=date(2025,1,1))
    ])
    v = crcl_cockcroft_gault(p)
    assert 60 < v < 80


def test_cg_mujer_factor():
    p = Paciente(pseudo_id="m", sexo="F", edad=65, peso_kg=80, labs=[
        LabResult(nombre="CREATININA EN SUERO U OTROS", valor=1.2, unidad="mg/dL", fecha=date(2025,1,1))
    ])
    v = crcl_cockcroft_gault(p)
    assert v is not None
    assert v < 70
