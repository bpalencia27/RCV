from datetime import date
from rcvco.domain.models import Paciente, LabResult
from rcvco.domain.tfg import crcl_cockcroft_gault


def test_crcl_cockcroft_gault():
    p = Paciente(
        pseudo_id="tfg1",
        sexo="M",
        edad=65,
        peso_kg=80,
        labs=[
            LabResult(
                nombre="CREATININA EN SUERO U OTROS",
                valor=1.2,
                unidad="mg/dL",
                fecha=date(2025, 1, 1),
            ),
        ],
    )
    crcl = crcl_cockcroft_gault(p)
    # Fórmula manual aproximada: ((140-65)*80)/(72*1.2) ~ 69.44
    assert 65 < crcl < 75
