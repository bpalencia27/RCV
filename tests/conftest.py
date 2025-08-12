"""Configuración global de pruebas para RCV-CO."""

import pytest
from datetime import datetime, date
from typing import Dict, List, Optional, Union

@pytest.fixture
def paciente_base():
    """Fixture con datos base de paciente para pruebas."""
    return {
        "edad": 65,
        "sexo": "m",
        "peso": 70,
        "talla": 1.70,
        "creatinina": 1.2,
        "fecha_ingreso": date(2025, 1, 1),
        "tiene_dm": False,
        "tiene_hta": False,
        "tiene_ecv": False,
        "tabaquismo": False,
        "fragil": False,
        "dano_organo": False,
        "pa_sistolica": 130,
        "pa_diastolica": 80,
        "laboratorios": []
    }

@pytest.fixture
def lab_base():
    """Fixture con resultados base de laboratorio para pruebas."""
    return {
        "glicemia": 95,
        "colesterol_total": 180,
        "colesterol_ldl": 100,
        "colesterol_hdl": 45,
        "trigliceridos": 140,
        "hba1c": 5.5,
        "rac": 25,
        "hemoglobina": 14,
        "hematocrito": 42,
        "pth": 45,
        "albumina": 4.0,
        "fosforo": 3.5,
        "fecha": date(2025, 1, 1)
    }
