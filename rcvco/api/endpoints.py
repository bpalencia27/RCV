from __future__ import annotations
from typing import List, Dict, Any
from pydantic import BaseModel
from rcvco.domain.models import Paciente, LabResult

# Almacenamiento en memoria (simple / no persistente)
_PACIENTES: Dict[str, Paciente] = {}

class PacienteIn(BaseModel):
    pseudo_id: str
    sexo: str
    edad: int
    peso_kg: float | None = None
    has_dm: bool = False
    has_hta: bool = False
    labs: List[Dict[str, Any]] = []

async def listar_pacientes(request) -> Any:  # Starlette Request
    return [p.model_dump() for p in _PACIENTES.values()]

async def crear_paciente(request) -> Any:
    data = await request.json()
    model = PacienteIn(**data)
    labs = [LabResult(**l) for l in model.labs]
    paciente = Paciente(
        pseudo_id=model.pseudo_id,
        sexo=model.sexo,
        edad=model.edad,
        peso_kg=model.peso_kg,
        has_dm=model.has_dm,
        has_hta=model.has_hta,
        labs=labs,
    )
    _PACIENTES[paciente.pseudo_id] = paciente
    return {"status": "ok", "paciente": paciente.model_dump()}

__all__ = ["listar_pacientes", "crear_paciente"]
