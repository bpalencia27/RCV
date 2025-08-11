from __future__ import annotations
import reflex as rx
import httpx

class ContentState(rx.State):
    about_md: str = ""
    home_notice: str = ""
    cargando: bool = False
    guardando: bool = False
    mensaje: str = ""

    async def cargar(self):  # type: ignore[override]
        self.cargando = True
        self.mensaje = ""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                    r = await client.get("/api/content")
            if r.status_code == 200:
                data = r.json()
                self.about_md = data.get("about_md", "")
                self.home_notice = data.get("home_notice", "")
            else:
                self.mensaje = f"Error HTTP {r.status_code} al cargar"
        except Exception as e:  # noqa: BLE001
            self.mensaje = f"Error: {e}"[:160]
        finally:
            self.cargando = False

    async def guardar(self):  # type: ignore[override]
        self.guardando = True
        self.mensaje = ""
        try:
            payload = {"about_md": self.about_md, "home_notice": self.home_notice}
            async with httpx.AsyncClient(timeout=10.0) as client:
                    r = await client.post("/api/content", json=payload)
            if r.status_code == 200:
                self.mensaje = "Guardado ✅"
            else:
                self.mensaje = f"Error HTTP {r.status_code} al guardar"
        except Exception as e:  # noqa: BLE001
            self.mensaje = f"Error: {e}"[:160]
        finally:
            self.guardando = False


def admin_content_page() -> rx.Component:
    return rx.box(
        rx.heading("Editor de Contenido", size="8", class_name="mb-6"),
        rx.vstack(
            rx.box(
                rx.heading("Aviso Inicio", size="4"),
                rx.text_area(value=ContentState.home_notice, on_change=ContentState.set_home_notice, height="100px", class_name="w-full input-field"),
                class_name="space-y-2",
            ),
            rx.box(
                rx.heading("Sección Acerca de (Markdown)", size="4"),
                rx.text_area(value=ContentState.about_md, on_change=ContentState.set_about_md, height="220px", class_name="w-full input-field"),
                class_name="space-y-2",
            ),
            rx.hstack(
                rx.button(rx.cond(ContentState.cargando, "Cargando...", "Recargar"), on_click=ContentState.cargar, disabled=ContentState.cargando),
                rx.button(rx.cond(ContentState.guardando, "Guardando...", "Guardar"), on_click=ContentState.guardar, disabled=ContentState.guardando, color_scheme="green"),
                rx.cond(ContentState.mensaje != "", rx.text(ContentState.mensaje, class_name="text-sm")),
                spacing="4",
            ),
            rx.divider(),
            rx.heading("Vista Previa 'Acerca de'", size="5"),
            rx.markdown(ContentState.about_md or "(Vacío)"),
            class_name="space-y-6 max-w-4xl",
        ),
        class_name="p-10 max-w-6xl mx-auto",
        on_mount=ContentState.cargar,
    )


def get_page():
    return admin_content_page()

__all__ = ["get_page", "admin_content_page", "ContentState"]
