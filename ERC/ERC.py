"""Aplicación principal RCV-CO integrada (sustituye pantalla por defecto)."""

from __future__ import annotations
import reflex as rx
from rcvco.ui.pages.paciente import get_page as paciente_page
from rcvco.ui.pages.cardiaia import get_page as cardiaia_page
from rcvco.api.endpoints import listar_pacientes, crear_paciente


class UIState(rx.State):
    """Estado de la UI."""
    dark: bool = True
    theme_text: str = "🌙"

    def toggle_theme(self):
        """Cambiar entre tema claro y oscuro."""
        self.dark = not self.dark
        self.theme_text = "🌙" if self.dark else "☀"


def get_theme_icon(state: UIState):
    return "🌙" if state.dark else "☀"

def index() -> rx.Component:
    menu_items = [
        ("Paciente", "/paciente"),
        ("CardiaIA (Reflex)", "/cardiaia"),
        ("CardiaIA HTML Legacy", "/legacy/cardiaia.html"),
        ("API Pacientes (GET)", "/api/pacientes"),
    ]
    
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("RCV-CO", size="8"),
                rx.spacer(),
                rx.button(
                    UIState.theme_text,
                    on_click=UIState.toggle_theme,
                ),
                width="100%",
                padding="1rem",
            ),
            rx.text(
                "Evaluación de Riesgo Cardiovascular y Enfermedad Renal Crónica",
                padding="0.5rem",
            ),
            rx.vstack(
                *[
                    rx.link(
                        text,
                        href=href,
                        padding="0.5rem",
                        _hover={"text_decoration": "underline"},
                    )
                    for text, href in menu_items
                ],
                spacing="2",
                padding="1rem",
            ),
            spacing="4",
            width="100%",
            align_items="stretch",
        ),
        width="100%",
    )


# Crear y configurar la aplicación
app = rx.App()

# Agregar páginas
app.add_page(
    index,
    route="/",
    title="Inicio",
)

app.add_page(
    paciente_page,
    route="/paciente",
    title="Paciente",
)

app.add_page(
    cardiaia_page,
    route="/cardiaia",
    title="CardiaIA",
)

# Configurar API endpoints
if app._api is not None:
    app._api.add_route("/api/pacientes", listar_pacientes, methods=["GET"])
    app._api.add_route("/api/pacientes", crear_paciente, methods=["POST"])
