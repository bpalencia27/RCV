"""Componentes modales reutilizables."""
from __future__ import annotations

import reflex as rx
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

from rcvco.ui.state.form_state import AppState, LabItem
from rcvco.ui.catalogs import LABS_MAP, LABS_FRECUENCIA
from rcvco.ui.types import EstadioERC

TZ_BOGOTA = ZoneInfo("America/Bogota")

def lab_modal() -> rx.Component:
    """Modal para agregar/editar laboratorio."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header("Laboratorio"),
                rx.modal_body(
                    rx.vstack(
                        # Selector laboratorio con unidades
                        rx.select(
                            list(LABS_MAP.keys()),
                            placeholder="Seleccione examen",
                            value=AppState.lab_edit_nombre,
                            on_change=AppState.set_lab_edit_nombre,
                            required=True,
                        ),
                        rx.hstack(
                            rx.number_input(
                                placeholder="Valor",
                                value=AppState.lab_edit_valor,
                                on_change=AppState.set_lab_edit_valor,
                                required=True,
                                min_=0,
                                step=0.1,
                            ),
                            rx.text(
                                lambda: LABS_MAP.get(AppState.lab_edit_nombre, ""),
                                color="gray.500",
                            ),
                            width="100%",
                        ),
                        rx.input(
                            type_="date",
                            value=AppState.lab_edit_fecha,
                            on_change=AppState.set_lab_edit_fecha,
                            required=True,
                            max_=datetime.now(TZ_BOGOTA).strftime("%Y-%m-%d"),
                        ),
                        width="100%",
                        spacing="4",
                    ),
                ),
                rx.modal_footer(
                    rx.button(
                        "Cancelar",
                        on_click=AppState.toggle_modal_labs,
                    ),
                    rx.button(
                        "Guardar",
                        on_click=AppState.save_lab,
                        color_scheme="blue",
                    ),
                ),
            ),
        ),
        is_open=AppState.modal_labs_abierto,
    )

def proximos_labs_modal() -> rx.Component:
    """Modal de agenda laboratorios."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header("Próximos Laboratorios"),
                rx.modal_body(
                    rx.vstack(
                        rx.text(
                            "Agenda según estadio y regla X-Y días",
                            mb="4",
                            color="gray.600",
                        ),
                        rx.data_table(
                            data=[
                                {
                                    "nombre": nombre,
                                    "fecha": AppState.proximo_labs.get(nombre, ""),
                                    "urgencia": "Vencido" if AppState.proximo_labs.get(nombre, "") < datetime.now(TZ_BOGOTA).strftime("%Y-%m-%d") else "Pendiente",
                                }
                                for nombre, freq in LABS_FRECUENCIA.items()
                                if nombre in AppState.proximo_labs
                            ],
                            columns=[
                                rx.data_column("Examen", "nombre"),
                                rx.data_column("Fecha", "fecha"),
                                rx.data_column(
                                    "Estado",
                                    "urgencia",
                                    cell=lambda item: rx.badge(
                                        item["urgencia"],
                                        color_scheme="red" if item["urgencia"] == "Vencido" else "yellow",
                                    ),
                                ),
                            ],
                            pagination=True,
                        ),
                        width="100%",
                    ),
                ),
                rx.modal_footer(
                    rx.button(
                        "Cerrar",
                        on_click=AppState.toggle_modal_labs_proximos,
                    ),
                ),
                size="xl",
            ),
        ),
        is_open=AppState.modal_labs_proximos_abierto,
    )

def fragilidad_modal() -> rx.Component:
    """Modal escala Fried."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header("Evaluación de Fragilidad"),
                rx.modal_body(
                    rx.vstack(
                        rx.text(
                            "Escala de Fried",
                            font_weight="bold",
                            mb="2",
                        ),
                        rx.checkbox(
                            "Pérdida de peso no intencional (>4.5kg en último año)",
                            is_checked=AppState.perdida_peso,
                            on_change=AppState.set_perdida_peso,
                        ),
                        rx.checkbox(
                            "Agotamiento autoreportado",
                            is_checked=AppState.agotamiento,
                            on_change=AppState.set_agotamiento,
                        ),
                        rx.checkbox(
                            "Debilidad muscular (↓fuerza prensión)",
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
                        rx.divider(),
                        rx.hstack(
                            rx.text(
                                "Estado:",
                                font_weight="bold",
                            ),
                            rx.badge(
                                "FRÁGIL" if AppState.es_fragil else "No frágil",
                                color_scheme="red" if AppState.es_fragil else "green",
                            ),
                            width="100%",
                            justify="space-between",
                        ),
                        width="100%",
                        spacing="4",
                        align_items="flex-start",
                    ),
                ),
                rx.modal_footer(
                    rx.button(
                        "Cerrar",
                        on_click=AppState.toggle_modal_fragilidad,
                    ),
                ),
            ),
        ),
        is_open=AppState.modal_fragilidad_abierto,
    )

def informe_modal() -> rx.Component:
    """Modal de informe generado."""
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header("Informe Médico"),
                rx.modal_body(
                    rx.cond(
                        AppState.generando_informe,
                        rx.center(
                            rx.circular_progress(
                                rx.circular_progress_label("Generando..."),
                                is_indeterminate=True,
                            ),
                            p="8",
                        ),
                        rx.vstack(
                            rx.html(AppState.informe_html),
                            rx.button(
                                "Descargar PDF",
                                on_click=AppState.download_informe,
                                color_scheme="blue",
                                is_disabled=not AppState.informe_html,
                            ),
                            width="100%",
                            spacing="4",
                        ),
                    ),
                ),
                rx.modal_footer(
                    rx.button(
                        "Cerrar",
                        on_click=AppState.toggle_modal_informe,
                    ),
                ),
                size="4xl",
            ),
        ),
        is_open=AppState.modal_informe_abierto,
    )

__all__ = [
    "lab_modal",
    "proximos_labs_modal",
    "fragilidad_modal", 
    "informe_modal"
]
