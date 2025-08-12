"""Componentes gestión medicamentos."""
from __future__ import annotations

import reflex as rx
from rcvco.ui.state.form_state import AppState, MedicamentoItem

def meds_panel() -> rx.Component:
    """Panel principal medicamentos."""
    return rx.vstack(
        rx.heading("Medicamentos", size="md"),
        rx.data_table(
            data=AppState.medicamentos,
            columns=[
                rx.data_column("Nombre", "nombre"),
                rx.data_column("Dosis", "dosis"),
                rx.data_column("Frecuencia", "frecuencia"),
                rx.data_column(
                    "Acciones",
                    cell=lambda item: rx.hstack(
                        rx.button(
                            "Editar",
                            on_click=lambda: AppState.edit_medicamento(item),
                            size="sm",
                        ),
                        rx.button(
                            "Eliminar",
                            on_click=lambda: AppState.remove_medicamento(item),
                            size="sm",
                            color_scheme="red",
                        ),
                    ),
                ),
            ],
            pagination=True,
            search=True,
        ),
        rx.button(
            "Agregar Medicamento",
            on_click=AppState.toggle_modal_meds,
        ),
        rx.button(
            "Sugerir Ajuste por TFG",
            on_click=AppState.suggest_dosing,
            is_disabled=not AppState.tfg_cg,
        ),
        width="100%",
        align_items="flex-start",
        spacing="4",
    )

def med_modal() -> rx.Component:
    """Modal edición medicamento."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header("Medicamento"),
                rx.modal_body(
                    rx.vstack(
                        rx.input(
                            placeholder="Nombre",
                            value=AppState.med_edit_nombre,
                            on_change=AppState.set_med_edit_nombre,
                            required=True,
                        ),
                        rx.input(
                            placeholder="Dosis",
                            value=AppState.med_edit_dosis,
                            on_change=AppState.set_med_edit_dosis,
                            required=True,
                        ),
                        rx.input(
                            placeholder="Frecuencia",
                            value=AppState.med_edit_frecuencia,
                            on_change=AppState.set_med_edit_frecuencia,
                            required=True,
                        ),
                        width="100%",
                        spacing="4",
                    ),
                ),
                rx.modal_footer(
                    rx.button(
                        "Cancelar",
                        on_click=AppState.toggle_modal_meds,
                    ),
                    rx.button(
                        "Guardar",
                        on_click=AppState.save_medicamento,
                        color_scheme="blue",
                    ),
                ),
            ),
        ),
        is_open=AppState.modal_meds_abierto,
    )

__all__ = ["meds_panel", "med_modal"]
