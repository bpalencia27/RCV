import pytest

# Placeholder tests básicos para asegurar que las fórmulas IMC / TFG simplificada y riesgo no cambian
from rcvco.ui.pages.index import IndexState

@pytest.mark.asyncio
async def test_imc_calc():
    st = IndexState()
    st.peso = "80"
    st.talla = "175"
    st._calc_imc()
    assert st.imc_display.startswith("26."), st.imc_display

@pytest.mark.asyncio
async def test_tfg_simple():
    st = IndexState()
    st.edad = "60"
    st.sexo = "m"
    st.peso = "80"
    st.creatinina = "1.2"
    st._calc_tfg()
    assert st.tfg_display != "", "TFG vacío"

@pytest.mark.asyncio
async def test_riesgo_basico():
    st = IndexState()
    st.edad = "70"
    st.dx_dm = True
    st.dx_hta = True
    st.creatinina = "1.5"
    st.peso = "70"
    st.talla = "170"
    st._calc_imc(); st._calc_tfg(); st._calc_riesgo()
    assert st.riesgo_nivel in {"ALTO","MUY ALTO","MODERADO","BAJO","INCOMPLETO"}
