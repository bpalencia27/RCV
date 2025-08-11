from datetime import date
from pathlib import Path
from rcvco.ingest.parsers import parse_txt


def test_parse_txt_creatinina_filtra_orina(tmp_path):
    contenido = """Creatinina suero|1.1|2025-01-01\nCreatinina orina parcial|50|2025-01-02\nLDL colesterol|140|2025-03-01"""
    f = tmp_path / "labs.txt"
    f.write_text(contenido, encoding="utf-8")
    p = parse_txt(str(f))
    nombres = {l.nombre for l in p.labs}
    assert "CREATININA EN SUERO U OTROS" in nombres
    # No debe mapear creatinina orina
    assert all("orina" not in l.nombre.lower() for l in p.labs)
