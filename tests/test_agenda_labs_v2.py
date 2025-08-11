from datetime import date
from rcvco.domain.rcv_rules import generar_agenda_avanzada


def test_agenda_ldl_e3b_180():
    base = date(2025, 1, 1)
    ag = generar_agenda_avanzada(base, estadio="E3B", tiene_dm=False)
    ldl = [a for a in ag if a.examen == "COLESTEROL LDL"][0]
    assert (ldl.fecha_programada - base).days == 180


def test_agenda_hba1c_solo_dm():
    base = date(2025, 1, 1)
    ag_no_dm = generar_agenda_avanzada(base, estadio="E3A", tiene_dm=False)
    assert all(a.examen != "HEMOGLOBINA GLICOSILADA (HBA1C)" for a in ag_no_dm)
    ag_dm = generar_agenda_avanzada(base, estadio="E3A", tiene_dm=True)
    assert any(a.examen == "HEMOGLOBINA GLICOSILADA (HBA1C)" for a in ag_dm)


def test_agenda_creatinina_rango_vencido():
    base = date(2025, 1, 1)
    hoy = date(2025, 5, 5)
    ag = generar_agenda_avanzada(base, estadio="E3A", tiene_dm=False, hoy=hoy)
    creat = [a for a in ag if a.examen == "CREATININA EN SUERO U OTROS"][0]
    assert creat.fecha_programada == date(2025, 5, 2)
