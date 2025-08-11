"""Estado central de la aplicación Reflex (esqueleto inicial PR1).

Este módulo define la clase AppState que mantendrá:
- Datos del paciente
- Lista de laboratorios cargados / normalizados
- Medicamentos actuales
- Cálculos derivados (riesgo CV, TFG, fragilidad, etc.)

Iteración PR1: solo placeholders y estructura; lógica se llenará en PRs posteriores.
"""
from __future__ import annotations
from typing import List, Optional
import reflex as rx

class LabItem(rx.Base):
    nombre: str
    valor: float | None = None
    unidad: str | None = None
    fecha: str | None = None  # ISO YYYY-MM-DD

class MedicamentoItem(rx.Base):
    nombre: str
    dosis: str | None = None
    frecuencia: str | None = None

class AppState(rx.State):
    paciente_nombre: str = ""
    paciente_edad: int | None = None
    paciente_sexo: str = ""  # 'M' / 'F'
    paciente_peso_kg: float | None = None

    labs: List[LabItem] = []
    medicamentos: List[MedicamentoItem] = []

    # Placeholders de cálculos
    riesgo_cv_categoria: str = ""
    tfg_cg: float | None = None
    es_fragil: bool = False

    # Flags UI
    modal_labs_abierto: bool = False
    modal_meds_abierto: bool = False

    def toggle_modal_labs(self):
        self.modal_labs_abierto = not self.modal_labs_abierto

    def toggle_modal_meds(self):
        self.modal_meds_abierto = not self.modal_meds_abierto

__all__ = ["AppState", "LabItem", "MedicamentoItem"]
