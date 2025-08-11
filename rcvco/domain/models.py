from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal
from datetime import date, datetime

LabNombre = Literal[
    "CREATININA EN SUERO U OTROS",
    "GLUCOSA EN AYUNAS",
    "HEMOGLOBINA GLICOSILADA (HBA1C)",
    "COLESTEROL LDL",
    "COLESTEROL HDL",
    "TRIGLICERIDOS",
    "PRESION ARTERIAL SISTOLICA",
    "PRESION ARTERIAL DIASTOLICA",
]


class LabResult(BaseModel):
    nombre: str = Field(..., description="Nombre estandarizado del examen")
    valor: float = Field(..., description="Valor numérico del resultado")
    unidad: Optional[str] = Field(None, description="Unidad reportada")
    fecha: date = Field(..., description="Fecha de toma de muestra")

    @field_validator("nombre")
    def normalizar_nombre(cls, v: str) -> str:  # type: ignore[override]
        return v.strip().upper()


class Paciente(BaseModel):
    pseudo_id: str = Field(..., description="Identificador anonimizado")
    sexo: Literal["M", "F"]
    edad: int = Field(..., ge=0, le=120)
    peso_kg: Optional[float] = Field(None, ge=20, le=400)
    talla_cm: Optional[float] = Field(None, ge=50, le=250)
    has_dm: bool = Field(False, description="Diagnóstico de diabetes mellitus")
    has_hta: bool = Field(False, description="Diagnóstico de hipertensión arterial")
    estadio_erc: Optional[int] = Field(None, ge=1, le=5, description="Estadio de enfermedad renal crónica (1-5)")
    labs: List[LabResult] = Field(default_factory=list)


class AgendaItem(BaseModel):
    examen: str
    fecha_programada: date
    motivo: str
    revision_fecha: date


class ResumenRiesgo(BaseModel):
    riesgo_categoria: str
    puntaje: int
    ascvd: Optional[float]
    aclaramiento_creatinina: Optional[float]
    agenda: List[AgendaItem] = []


class Informe(BaseModel):
    generado_en: datetime
    texto: str


from typing import Dict, Any
from pydantic import Field

class AsistenteResultado(BaseModel):
    """Modelo único de salida del asistente.

    Campos compatibles con expectativas de tests: version (alias resumen/encabezado puede mapearse externamente),
    programa, riesgo, puntaje_total, faltantes, agenda, recomendaciones, datos_normalizados.
    """
    version: str = "v2.0"                    # versión lógica
    resumen: str = ""                        # texto corto
    programa: str = ""                       # programa prioritario
    riesgo: Optional[ResumenRiesgo] = None
    puntaje_total: int = 0
    faltantes: List[str] = Field(default_factory=list)
    agenda: List[AgendaItem] = Field(default_factory=list)
    recomendaciones: List[str] = Field(default_factory=list)
    datos_normalizados: Dict[str, Any] = Field(default_factory=dict)
    puntuacion_metas: Dict[str, Any] = Field(default_factory=dict)
    riesgo_cv: Dict[str, Any] = Field(default_factory=dict)
    alertas_tfg: List[str] = Field(default_factory=list)

__all__ = ["LabResult", "Paciente", "AgendaItem", "ResumenRiesgo", "Informe", "AsistenteResultado"]
