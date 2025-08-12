"""Componentes de formularios básicos."""
from __future__ import annotations

import reflex as rx
from rcvco.ui.state.form_state import AppState
from rcvco.ui.types import Sexo

def patient_form() -> rx.Component:
    """Formulario datos básicos paciente."""
    return rx.vstack(
        rx.hstack(
            rx.input(
                placeholder="Nombre",
                value=AppState.paciente_nombre,
                on_change=AppState.set_paciente_nombre,
                required=True,
                width="100%",
            ),
            rx.select(
                [e.value for e in Sexo],
                placeholder="Sexo",
                value=AppState.paciente_sexo,
                on_change=AppState.set_paciente_sexo,
                required=True,
            ),
            width="100%",
            spacing="4",
        ),
        rx.hstack(
            rx.number_input(
                placeholder="Edad",
                value=AppState.paciente_edad,
                on_change=AppState.set_paciente_edad,
                min_=1,
                max_=120,
                required=True,
            ),
            rx.number_input(
                placeholder="Peso (kg)",
                value=AppState.paciente_peso_kg,
                on_change=AppState.set_paciente_peso_kg,
                min_=20,
                max_=300,
                step=0.1,
                required=True,
            ),
            rx.number_input(
                placeholder="Talla (m)",
                value=AppState.paciente_talla_m,
                on_change=AppState.set_paciente_talla_m,
                min_=0.5,
                max_=2.5,
                step=0.01,
                required=True,
            ),
            width="100%",
            spacing="4",
        ),
        rx.hstack(
            rx.checkbox(
                "Diabetes Mellitus",
                is_checked=AppState.dx_dm,
                on_change=AppState.set_dx_dm,
            ),
            rx.checkbox(
                "Hipertensión",
                is_checked=AppState.dx_hta,
                on_change=AppState.set_dx_hta,
            ),
            rx.checkbox(
                "ERC",
                is_checked=AppState.dx_erc,
                on_change=AppState.set_dx_erc,
            ),
            rx.checkbox(
                "ECV establecida",
                is_checked=AppState.dx_cardiovascular,
                on_change=AppState.set_dx_cardiovascular,
            ),
            width="100%",
            spacing="4",
            wrap="wrap",
        ),
        width="100%",
        align_items="flex-start",
        spacing="4",
    )

def fragilidad_form() -> rx.Component:
    """Formulario criterios Fried."""
    return rx.vstack(
        rx.text("Criterios de Fragilidad (Fried)", as_="h3", font_weight="bold"),
        rx.checkbox(
            "Pérdida de peso no intencional",
            is_checked=AppState.perdida_peso,
            on_change=AppState.set_perdida_peso,
        ),
        rx.checkbox(
            "Agotamiento auto-reportado",
            is_checked=AppState.agotamiento,
            on_change=AppState.set_agotamiento,
        ),
        rx.checkbox(
            "Debilidad muscular",
            is_checked=AppState.debilidad,
            on_change=AppState.set_debilidad,
        ),
        rx.checkbox(
            "Lentitud en marcha",
            is_checked=AppState.lentitud,
            on_change=AppState.set_lentitud,
        ),
        rx.checkbox(
            "Baja actividad física",
            is_checked=AppState.inactividad,
            on_change=AppState.set_inactividad,
        ),
        rx.text(
            "Frágil: ≥3 criterios",
            color="gray.500",
            font_size="sm",
        ),
        width="100%",
        align_items="flex-start",
        spacing="3",
    )

def labs_form() -> rx.Component:
    """Formulario ingreso manual laboratorios."""
    return rx.vstack(
        rx.text("Laboratorios", as_="h3", font_weight="bold"),
        rx.data_table(
            data=AppState.labs,
            columns=[
                rx.data_column("Examen", "nombre"),
                rx.data_column("Valor", "valor"),
                rx.data_column("Unidad", "unidad"),
                rx.data_column("Fecha", "fecha"),
            ],
            on_row_click=AppState.edit_lab,
            pagination=True,
            search=True,
        ),
        rx.button(
            "Agregar Laboratorio",
            on_click=AppState.toggle_modal_labs,
        ),
        width="100%",
        align_items="flex-start",
        spacing="4",
    )

__all__ = ["patient_form", "fragilidad_form", "labs_form"]
