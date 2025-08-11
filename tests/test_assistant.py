from datetime import date
from rcvco.domain.models import Paciente, LabResult
from rcvco.domain.assistant import analizar_paciente

def test_analizar_paciente_generico():
    p = Paciente(
        pseudo_id="a1",
        sexo="M",
        edad=70,
        peso_kg=78,
        has_dm=True,
        has_hta=True,
        estadio_erc=3,
        labs=[
            LabResult(nombre="CREATININA EN SUERO U OTROS", valor=1.4, unidad="mg/dL", fecha=date(2025,5,1)),
            LabResult(nombre="HEMOGLOBINA GLICOSILADA (HBA1C)", valor=7.5, unidad="%", fecha=date(2025,4,15)),
            LabResult(nombre="COLESTEROL LDL", valor=150, unidad="mg/dL", fecha=date(2025,3,20)),
            LabResult(nombre="PRESION ARTERIAL SISTOLICA", valor=155, unidad="mmHg", fecha=date(2025,6,1)),
        ]
    )
    r = analizar_paciente(p)
    assert r.version == "v2.0"
    assert r.puntuacion_metas["programa"] == "ERC"
    assert any("LDL" in m for m in r.puntuacion_metas["metas_incumplidas"])  # meta LDL
    assert r.riesgo_cv["categoria"] in {"Muy Alto","Alto","Moderado","Bajo"}
    if r.alertas_tfg:
        assert any("Aclaramiento" in a for a in r.alertas_tfg)
    assert "Riesgo" in r.riesgo_cv["justificacion"]
