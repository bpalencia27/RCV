"""Panel de riesgo CV y metas."""
from __future__ import annotations

import reflex as rx
from rcvco.ui.state.form_state import AppState
from rcvco.ui.types import RiesgoCV

def risk_panel() -> rx.Component:
    """Panel principal de riesgo CV."""
    return rx.box(
        rx.vstack(
            # Cabecera con nivel de riesgo
            rx.hstack(
                rx.heading(
                    "Riesgo Cardiovascular",
                    size="lg",
                ),
                rx.spacer(),
                rx.badge(
                    AppState.riesgo_cv_categoria or "Incompleto",
                    color_scheme={
                        RiesgoCV.MUY_ALTO.value: "red",
                        RiesgoCV.ALTO.value: "orange",
                        RiesgoCV.MODERADO.value: "yellow",
                        RiesgoCV.BAJO.value: "green",
                    }.get(AppState.riesgo_cv_categoria, "gray"),
                    size="lg",
                ),
                width="100%",
            ),
            # Justificación (sin mencionar "pasos")
            rx.text(
                AppState.riesgo_justificacion or "Pendiente calcular riesgo",
                color="gray.600",
                _dark={"color": "gray.400"},
            ),
            # Panel de metas específicas según programa
            rx.box(
                rx.heading("Metas Terapéuticas", size="md", mb="4"),
                rx.wrap(
                    # PA
                    rx.box(
                        rx.stat(
                            rx.stat_label("Presión Arterial"),
                            rx.stat_number(f"{AppState.meta_pa_sys}/{AppState.meta_pa_dia}"),
                            rx.stat_help_text(
                                rx.badge(
                                    "Cumple" if AppState.pa_control_ok else "No cumple",
                                    color_scheme="green" if AppState.pa_control_ok else "red",
                                )
                            ),
                        ),
                        p="4",
                        border="1px",
                        border_color="gray.200",
                        rounded="md",
                    ),
                    # LDL 
                    rx.box(
                        rx.stat(
                            rx.stat_label("LDL"),
                            rx.stat_number(f"≤{AppState.meta_ldl} mg/dL"),
                            rx.stat_help_text(
                                rx.badge(
                                    "Cumple" if AppState.ldl_control_ok else "No cumple",
                                    color_scheme="green" if AppState.ldl_control_ok else "red",
                                )
                            ),
                        ),
                        p="4", 
                        border="1px",
                        border_color="gray.200",
                        rounded="md",
                    ),
                    # HbA1c (solo si DM)
                    rx.cond(
                        AppState.dx_dm,
                        rx.box(
                            rx.stat(
                                rx.stat_label("HbA1c"),
                                rx.stat_number(f"≤{AppState.meta_hba1c}%"),
                                rx.stat_help_text("según edad/comorbilidad"),
                            ),
                            p="4",
                            border="1px", 
                            border_color="gray.200",
                            rounded="md",
                        ),
                    ),
                    spacing="4",
                ),
                mt="6",
                p="4",
                border="1px",
                border_color="gray.200",
                rounded="lg",
                bg="white",
                _dark={"bg": "gray.800"},
            ),
            width="100%",
            spacing="6",
            align_items="stretch",
        ),
        width="100%",
        p="6",
        border="1px",
        border_color="gray.200",
        rounded="xl",
        bg="white",
        _dark={"bg": "gray.800"},
    )

__all__ = ["risk_panel"]
