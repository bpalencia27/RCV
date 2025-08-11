from __future__ import annotations
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any
from rcvco.services.report_service import build_and_generate_report, build_prompt
from rcvco.services.patient_service import merge_patient_data
from rcvco.parsing.parser import parse_document
from rcvco.adapters.llm.factory import get_llm_client
from rcvco.services.content_service import load_content, save_content

api_router = APIRouter()

from rcvco.api.schemas.patient import PatientRequest, ReportResponse, MedicationList


@api_router.post("/api/parse-text")
async def parse_text(raw: str):
    """Parseo muy básico de texto plano de laboratorio (placeholder).

    Busca patrones simples tipo 'LDL: 120 mg/dL' y construye JSON homogéneo.
    """
    import re
    patterns = {
        "CREATININA EN SUERO U OTROS": r"creatinina[^0-9]*([0-9]+\.?[0-9]*)",
        "HEMOGLOBINA GLICOSILADA (HBA1C)": r"hba1c[^0-9]*([0-9]+\.?[0-9]*)",
        "COLESTEROL LDL": r"ldl[^0-9]*([0-9]+\.?[0-9]*)",
    }
    labs: list[dict[str, Any]] = []
    lower = raw.lower()
    for nombre, pat in patterns.items():
        m = re.search(pat, lower)
        if m:
            try:
                valor = float(m.group(1))
            except Exception:
                continue
            labs.append({"nombre": nombre, "valor": valor})
    return {"labs": labs}


@api_router.post("/api/preview-report")
async def preview_report(data: Dict[str, Any]):
    """Devuelve prompt construido sin llamar al LLM (depuración UI)."""
    return {"prompt": build_prompt(data)}

@api_router.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    parsed = parse_document(content, file.filename)
    return parsed

@api_router.post("/api/report", response_model=ReportResponse)
async def report(data: PatientRequest):
    llm = get_llm_client()
    patient_model = merge_patient_data(data.model_dump())
    report_text = build_and_generate_report(llm, patient_model)
    return ReportResponse(report_text=report_text)

_medications: set[str] = set()

@api_router.post("/api/medications", response_model=MedicationList)
async def add_medication(name: str):
    norm = name.strip().lower()
    if not norm:
        raise HTTPException(status_code=400, detail="Nombre vacío")
    before = len(_medications)
    _medications.add(norm)
    return MedicationList(items=sorted(_medications))

@api_router.delete("/api/medications/{name}", response_model=MedicationList)
async def delete_medication(name: str):
    norm = name.strip().lower()
    _medications.discard(norm)
    return MedicationList(items=sorted(_medications))


# --- Contenido editable (simple) ---
@api_router.get("/api/content")
async def get_content():
    return load_content()


@api_router.post("/api/content")
async def post_content(data: Dict[str, Any]):
    save_content(data)
    return {"ok": True}
