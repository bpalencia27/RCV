from rcvco.ui.calculos import calc_imc, calc_tfg, calc_riesgo


def test_imc_basic():
    assert calc_imc("70", "170") == "24.2"
    assert calc_imc("", "170") == ""
    assert calc_imc("80", "0") == ""


def test_tfg_male():
    # Edad 60, peso 80, creatinina 1.0 -> ((140-60)*80)/(72*1)= (80*80)/72=6400/72≈88 -> 88 ml/min
    assert calc_tfg("60", "80", "1.0", "m").startswith("88")
    # Female factor 0.85 reduces
    val_f = calc_tfg("60", "80", "1.0", "f")
    assert val_f.endswith("ml/min") and int(val_f.split()[0]) < 88


def test_riesgo_scoring_muy_alto():
    # Build scenario expecting MUY ALTO (puntaje >=10)
    nivel, factores, meta = calc_riesgo(
        dx_dm=True,  # +2
        dx_hta=True,  # +1
        dx_erc=True,  # +2
        ecv_establecida=True,  # +4
        edad="70",  # +2 (>65)
        tfg_display="55 ml/min",  # +2 (<60)
        rac="40",  # +2 (>30)
        hba1c="9",  # +1 (>8 si DM)
        ldl="170",  # +1 (>160)
    )
    # Nota: la suma excede 10 ampliamente; verificamos clasificación
    assert nivel == "MUY ALTO"
    assert meta == 55
    assert "Diabetes" in factores


def test_riesgo_incompleto():
    nivel, factores, meta = calc_riesgo(
        dx_dm=False,
        dx_hta=False,
        dx_erc=False,
        ecv_establecida=False,
        edad="",
        tfg_display="",
        rac="",
        hba1c="",
        ldl="",
    )
    assert nivel == "INCOMPLETO"
    assert meta == 70
