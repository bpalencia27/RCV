"""Pruebas para la clasificación de riesgo cardiovascular usando el protocolo de 4 pasos."""

import pytest
from datetime import datetime, date
from rcvco.core.riesgo import clasificar_riesgo_cv_4_pasos

def test_riesgo_muy_alto_ecv():
    """Prueba clasificación MUY ALTO por ECV establecida."""
    riesgo = clasificar_riesgo_cv_4_pasos(
        tfg=65,
        tiene_ecv=True,
        tiene_dm=False,
        tiene_hta=False,
        dano_organo=False,
        duracion_dm_10_anos=False,
        pa_sistolica=130,
        pa_diastolica=80,
        ldl=100,
        factores_riesgo=1,
        rac=25
    )
    assert riesgo["nivel"] == "MUY ALTO"
    assert "ECV establecida" in riesgo["justificacion"]

def test_riesgo_muy_alto_tfg():
    """Prueba clasificación MUY ALTO por TFG ≤ 30."""
    riesgo = clasificar_riesgo_cv_4_pasos(
        tfg=25,
        tiene_ecv=False,
        tiene_dm=False,
        tiene_hta=False,
        dano_organo=False,
        duracion_dm_10_anos=False,
        pa_sistolica=130,
        pa_diastolica=80,
        ldl=100,
        factores_riesgo=1,
        rac=25
    )
    assert riesgo["nivel"] == "MUY ALTO"
    assert "TFG ≤ 30" in riesgo["justificacion"]

def test_riesgo_muy_alto_dm():
    """Prueba clasificación MUY ALTO por DM con daño de órgano."""
    riesgo = clasificar_riesgo_cv_4_pasos(
        tfg=65,
        tiene_ecv=False,
        tiene_dm=True,
        tiene_hta=False,
        dano_organo=True,
        duracion_dm_10_anos=False,
        pa_sistolica=130,
        pa_diastolica=80,
        ldl=100,
        factores_riesgo=1,
        rac=25
    )
    assert riesgo["nivel"] == "MUY ALTO"
    assert "Diabetes con daño de órgano" in riesgo["justificacion"]

def test_riesgo_alto_tfg():
    """Prueba clasificación ALTO por TFG 30-60."""
    riesgo = clasificar_riesgo_cv_4_pasos(
        tfg=45,
        tiene_ecv=False,
        tiene_dm=False,
        tiene_hta=False,
        dano_organo=False,
        duracion_dm_10_anos=False,
        pa_sistolica=130,
        pa_diastolica=80,
        ldl=100,
        factores_riesgo=1,
        rac=25
    )
    assert riesgo["nivel"] == "ALTO"
    assert "TFG entre 30-60" in riesgo["justificacion"]

def test_riesgo_alto_pa():
    """Prueba clasificación ALTO por PA ≥ 180/110."""
    riesgo = clasificar_riesgo_cv_4_pasos(
        tfg=65,
        tiene_ecv=False,
        tiene_dm=False,
        tiene_hta=True,
        dano_organo=False,
        duracion_dm_10_anos=False,
        pa_sistolica=180,
        pa_diastolica=110,
        ldl=100,
        factores_riesgo=1,
        rac=25
    )
    assert riesgo["nivel"] == "ALTO"
    assert "PA ≥ 180/110" in riesgo["justificacion"]

def test_riesgo_moderado_potenciadores():
    """Prueba clasificación MODERADO por 1-2 potenciadores."""
    riesgo = clasificar_riesgo_cv_4_pasos(
        tfg=65,
        tiene_ecv=False,
        tiene_dm=False,
        tiene_hta=False,
        dano_organo=False,
        duracion_dm_10_anos=False,
        pa_sistolica=130,
        pa_diastolica=80,
        ldl=100,
        factores_riesgo=2,
        rac=25
    )
    assert riesgo["nivel"] == "MODERADO"
    assert "factores de riesgo" in riesgo["justificacion"].lower()

def test_riesgo_bajo():
    """Prueba clasificación BAJO sin factores significativos."""
    riesgo = clasificar_riesgo_cv_4_pasos(
        tfg=65,
        tiene_ecv=False,
        tiene_dm=False,
        tiene_hta=False,
        dano_organo=False,
        duracion_dm_10_anos=False,
        pa_sistolica=120,
        pa_diastolica=75,
        ldl=100,
        factores_riesgo=0,
        rac=25
    )
    assert riesgo["nivel"] == "BAJO"
