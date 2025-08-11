"""UI Bridge: adapta JSON de entrada de la página CardiaIA a modelos y lógica de dominio."""
from __future__ import annotations
from datetime import date
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError
from rcvco.domain.tfg import crcl_cockcroft_gault
from rcvco.domain.scoring import calcula_puntaje
from rcvco.domain.risk import clasificar_riesgo_cv_4_pasos, ascvd_ajustado
from rcvco.domain.rcv_rules import generar_agenda_avanzada
from rcvco.domain.models import Paciente, LabResult


class PatientInput(BaseModel):
    id: str = Field(..., alias="id")
    sexo: str
    edad: int
    pesoKg: Optional[float] = None
    creatininaMgDl: Optional[float] = None
    estadioERC: Optional[str] = None
    tfgeMlMin: Optional[float] = None
    tieneDM: bool = False
    tieneHTA: bool = False
    paSistolica: Optional[float] = None
    paDiastolica: Optional[float] = None
    ldl: Optional[float] = None
    ldlPrevio: Optional[float] = None
    hdl: Optional[float] = None
    tg: Optional[float] = None
    glicemia: Optional[float] = None
    hba1c: Optional[float] = None
    racMgG: Optional[float] = None
    imc: Optional[float] = None
    circAbdomenCm: Optional[float] = None
    fechaActual: date
    fechaIngreso: Optional[date] = None

    class Config:
        allow_population_by_field_name = True


def _build_paciente(pi: PatientInput) -> Paciente:
    labs: List[LabResult] = []
    fa = pi.fechaActual
    def add(nombre: str, valor: Optional[float], unidad: str = ""):
        if valor is not None:
            labs.append(LabResult(nombre=nombre, valor=valor, unidad=unidad, fecha=fa))
    add("CREATININA EN SUERO U OTROS", pi.creatininaMgDl, "mg/dL")
    add("COLESTEROL LDL", pi.ldl, "mg/dL")
    add("HEMOGLOBINA GLICOSILADA (HBA1C)", pi.hba1c, "%")
    add("PRESION ARTERIAL SISTOLICA", pi.paSistolica, "mmHg")
    add("PRESION ARTERIAL DIASTOLICA", pi.paDiastolica, "mmHg")
    return Paciente(pseudo_id=pi.id, sexo=pi.sexo.upper()[0], edad=pi.edad, peso_kg=pi.pesoKg, labs=labs)


def _programa_prioritario(pi: PatientInput) -> str:
    if pi.estadioERC and pi.estadioERC.upper().startswith("E") and pi.estadioERC != "E0":
        return "ERC"
    if pi.tieneDM:
        return "DM"
    if pi.tieneHTA:
        return "HTA"
    return "GENERAL"


def procesar_json(data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        pi = PatientInput.parse_obj(data)
    except ValidationError as e:
        return {"error": "Validación", "detalles": e.errors()}
    paciente = _build_paciente(pi)
    puntaje = calcula_puntaje(paciente)
    riesgo_cat = clasificar_riesgo_cv_4_pasos(paciente)
    ascvd = ascvd_ajustado(paciente)
    crcl = crcl_cockcroft_gault(paciente, creatinina_mg_dl=pi.creatininaMgDl) if pi.creatininaMgDl else None
    programa = _programa_prioritario(pi)
    agenda = generar_agenda_avanzada(
        fecha_base=pi.fechaActual,
        estadio=pi.estadioERC or "E1",
        tiene_dm=pi.tieneDM,
        ldl_val=pi.ldl,
    )
    # model_dump(mode="json") garantiza serialización ISO de fechas
    return {
        "encabezado": "RCV-CO Asistente v2.0",
        "programaPrioritario": programa,
        "riesgo": {"categoria": riesgo_cat, "puntaje": puntaje, "ascvd": ascvd},
        "funcionRenal": {"crcl": crcl, "ajusteMedicacion": bool(crcl is not None and crcl < 45)},
        "agenda": [a.model_dump(mode="json") for a in agenda],
    }

__all__ = ["procesar_json", "PatientInput"]
