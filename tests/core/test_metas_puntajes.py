"""Pruebas para la clasificación de metas y puntuaciones por programa."""

import pytest
from datetime import datetime, date
from rcvco.core.metas import calcular_puntuacion_metas

def test_metas_hta():
    """Prueba puntuación para programa HTA."""
    puntos = calcular_puntuacion_metas(
        programa="HTA",
        tfg=65,
        glicemia=90,
        ldl_actual=100,
        ldl_previo=200,
        hdl=45,
        trigliceridos=140,
        pa_sistolica=135,
        pa_diastolica=85,
        rac=25,
        peso_actual=70,
        peso_previo=75,
        perimetro=92,
        sexo="m",
        edad=55,
        riesgo_cv="ALTO"
    )
    assert isinstance(puntos, dict)
    assert "total" in puntos
    assert puntos["total"] > 0
    assert puntos["glicemia"] == 5  # 60-100 mg/dl
    assert puntos["ldl"] == 25      # ↓≥50% vs previo
    assert puntos["pa"] == 25       # ≤140/90 si <60 años

def test_metas_dm():
    """Prueba puntuación para programa DM."""
    puntos = calcular_puntuacion_metas(
        programa="DM",
        tfg=65,
        glicemia=110,
        ldl_actual=95,
        ldl_previo=120,
        hdl=45,
        trigliceridos=140,
        pa_sistolica=135,
        pa_diastolica=85,
        rac=25,
        peso_actual=70,
        peso_previo=75,
        perimetro=92,
        sexo="m",
        edad=55,
        hba1c=6.5,
        tiene_ecv=False
    )
    assert isinstance(puntos, dict)
    assert "total" in puntos
    assert puntos["total"] > 0
    assert puntos["glicemia"] == 4   # 70-130 mg/dl
    assert puntos["ldl"] == 20       # ≤100 mantener
    assert puntos["hba1c"] == 20     # ≤7% si ≤65 y sin ECV

def test_metas_erc_e4_dm():
    """Prueba puntuación para ERC estadio 4 con DM."""
    puntos = calcular_puntuacion_metas(
        programa="ERC",
        tfg=25,  # E4
        glicemia=110,
        ldl_actual=95,
        ldl_previo=120,
        hdl=45,
        trigliceridos=140,
        pa_sistolica=135,
        pa_diastolica=85,
        rac=25,
        peso_actual=70,
        peso_previo=75,
        perimetro=92,
        sexo="m",
        edad=55,
        hba1c=6.5,
        tiene_dm=True
    )
    assert isinstance(puntos, dict)
    assert "total" in puntos
    assert puntos["total"] > 0
    assert puntos["glicemia"] == 5   # Menor peso en E4
    assert puntos["ldl"] == 0        # Sin puntos LDL en E4
    assert puntos["pa"] == 30        # Mayor peso PA en E4
    assert puntos["hba1c"] == 30     # Mayor peso HbA1c en E4 con DM

def test_validacion_programa():
    """Prueba validación de programa inválido."""
    with pytest.raises(ValueError):
        calcular_puntuacion_metas(
            programa="INVALID",
            tfg=65,
            glicemia=90,
            ldl_actual=100,
            ldl_previo=120,
            hdl=45,
            trigliceridos=140,
            pa_sistolica=135,
            pa_diastolica=85,
            rac=25,
            peso_actual=70,
            peso_previo=75,
            perimetro=92,
            sexo="m",
            edad=55
        )
