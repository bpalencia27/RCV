from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional

class LabIn(BaseModel):
    nombre: str
    valor: float
    unidad: Optional[str] = None
    fecha: Optional[str] = None  # ISO string

class PatientRequest(BaseModel):
    pseudo_id: str
    sexo: str = Field(pattern='^[MFmf]$')
    edad: int = Field(ge=0, le=120)
    peso_kg: Optional[float] = Field(None, ge=20, le=400)
    has_dm: bool = False
    has_hta: bool = False
    labs: List[LabIn] = Field(default_factory=list)
    medications: List[str] = Field(default_factory=list)

class ReportResponse(BaseModel):
    report_text: str

class MedicationList(BaseModel):
    items: List[str]

__all__ = [
    'LabIn','PatientRequest','ReportResponse','MedicationList'
]
