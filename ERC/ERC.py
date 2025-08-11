"""Aplicación principal RCV-CO integrada (sustituye pantalla por defecto)."""

from __future__ import annotations
import reflex as rx
from rcvco.ui.pages.paciente import get_page as paciente_page
from rcvco.ui.pages.cardiaia import get_page as cardiaia_page
from rcvco.ui.pages.index import get_page as index_page
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
    # Reemplazado por página index avanzada (index_page)
    return index_page()


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
