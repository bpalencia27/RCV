from __future__ import annotations
import re
from datetime import datetime
from pathlib import Path
from typing import List
from pydantic import BaseModel
from rcvco.domain.models import Paciente, LabResult

# Mapeo simple nombres -> etiqueta estandarizada
MAP_NOMBRES = {
    re.compile(r"creatinina.*suero", re.I): "CREATININA EN SUERO U OTROS",
    re.compile(r"hba1c|hemoglobina glic", re.I): "HEMOGLOBINA GLICOSILADA (HBA1C)",
    re.compile(r"glucosa", re.I): "GLUCOSA EN AYUNAS",
    re.compile(r"ldl", re.I): "COLESTEROL LDL",
    re.compile(r"hdl", re.I): "COLESTEROL HDL",
    re.compile(r"triglic", re.I): "TRIGLICERIDOS",
    re.compile(r"presion.*sistol", re.I): "PRESION ARTERIAL SISTOLICA",
    re.compile(r"presion.*diastol", re.I): "PRESION ARTERIAL DIASTOLICA",
}

RE_FECHA = re.compile(r"(\d{4}-\d{2}-\d{2})")
RE_VALOR = re.compile(r"([0-9]+(?:\.[0-9]+)?)")


def _mapear_nombre(original: str) -> str | None:
    o = original.strip().lower()
    # descartar creatinina orina parcial
    if "creatinina" in o and "orina" in o:
        return None
    for pat, estandar in MAP_NOMBRES.items():
        if pat.search(original):
            return estandar
    return None


def parse_txt(path: str, pseudo_id: str = "anon", sexo: str = "M", edad: int = 50) -> Paciente:
    contenido = Path(path).read_text(encoding="utf-8", errors="ignore")
    labs: List[LabResult] = []
    for linea in contenido.splitlines():
        partes = linea.split("|")
        if len(partes) < 2:
            continue
        nombre_raw = partes[0]
        nombre = _mapear_nombre(nombre_raw)
        if not nombre:
            continue
        match_v = RE_VALOR.search(partes[1])
        match_f = RE_FECHA.search(linea)
        if not match_v:
            continue
        valor = float(match_v.group(1))
        fecha = (
            datetime.strptime(match_f.group(1), "%Y-%m-%d").date()
            if match_f
            else datetime.today().date()
        )
        labs.append(LabResult(nombre=nombre, valor=valor, unidad="", fecha=fecha))
    return Paciente(pseudo_id=pseudo_id, sexo=sexo, edad=edad, labs=labs)


def parse_pdf(path: str, **kwargs) -> Paciente:
    # Placeholder: tratar PDF como texto plano (se podría integrar pdfplumber)
    return parse_txt(path, **kwargs)


__all__ = ["parse_txt", "parse_pdf"]
