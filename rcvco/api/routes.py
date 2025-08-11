from __future__ import annotations
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from rcvco.services.report_service import build_and_generate_report
from rcvco.services.patient_service import merge_patient_data
from rcvco.parsing.parser import parse_document
from rcvco.adapters.llm.factory import get_llm_client

api_router = APIRouter()

from rcvco.api.schemas.patient import PatientRequest, ReportResponse, MedicationList

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
