"""Pruebas para el cálculo de la TFG usando la fórmula de Cockcroft-Gault."""

import pytest
from datetime import datetime, date
from rcvco.core.calculos import calcular_tfg_cg

def test_calculo_tfg_hombre():
    """Prueba el cálculo de TFG para un hombre."""
    tfg = calcular_tfg_cg(
        creatinina=1.2,  # mg/dL
        edad=65,         # años
        sexo="m",
        peso=70         # kg
    )
    assert round(tfg, 1) == 55.6  # ml/min

def test_calculo_tfg_mujer():
    """Prueba el cálculo de TFG para una mujer (ajuste x0.85)."""
    tfg = calcular_tfg_cg(
        creatinina=1.2,  # mg/dL
        edad=65,         # años
        sexo="f",
        peso=70         # kg
    )
    assert round(tfg, 1) == 47.2  # ml/min

def test_valores_invalidos():
    """Prueba el manejo de valores inválidos."""
    with pytest.raises(ValueError):
        calcular_tfg_cg(creatinina=0, edad=65, sexo="m", peso=70)
    
    with pytest.raises(ValueError):
        calcular_tfg_cg(creatinina=1.2, edad=0, sexo="m", peso=70)
        
    with pytest.raises(ValueError):
        calcular_tfg_cg(creatinina=1.2, edad=65, sexo="x", peso=70)
        
    with pytest.raises(ValueError):
        calcular_tfg_cg(creatinina=1.2, edad=65, sexo="m", peso=0)

def test_tipos_datos():
    """Prueba el manejo de diferentes tipos de datos."""
    tfg_str = calcular_tfg_cg(
        creatinina="1.2",
        edad="65",
        sexo="m", 
        peso="70"
    )
    tfg_float = calcular_tfg_cg(
        creatinina=1.2,
        edad=65,
        sexo="m",
        peso=70.0
    )
    assert round(tfg_str, 1) == round(tfg_float, 1)

def test_casos_borde():
    """Prueba casos límite de TFG."""
    # Creatinina alta (5 mg/dL) - TFG muy baja
    tfg_bajo = calcular_tfg_cg(
        creatinina=5.0,
        edad=65,
        sexo="m",
        peso=70
    )
    assert tfg_bajo < 20  # Debería estar en rango de prediálisis
    
    # Creatinina baja (0.5 mg/dL) - TFG alta
    tfg_alto = calcular_tfg_cg(
        creatinina=0.5,
        edad=25,
        sexo="m",
        peso=70
    )
    assert tfg_alto > 90  # Debería estar en estadio 1
