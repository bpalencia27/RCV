from rcvco.parsing.labs import normalize_lab_name


def test_creatinina_variants():
    variants = ["creat", "creatinina", "crea", "CREAT"]
    for v in variants:
        assert normalize_lab_name(v) == "CREATININA EN SUERO U OTROS"


def test_unknown_passthrough():
    assert normalize_lab_name("glucosa") == "GLUCOSA"
