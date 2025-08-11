"""Página Reflex CardiaIA: replica UX legacy con formulario JSON y resultados."""
from __future__ import annotations
import json
import reflex as rx
from rcvco.adapters.ui_bridge import procesar_json


class CardiaState(rx.State):
    input_json: str = "{\n  \"id\": \"P-001\",\n  \"sexo\": \"M\",\n  \"edad\": 68,\n  \"pesoKg\": 70,\n  \"creatininaMgDl\": 2.0,\n  \"estadioERC\": \"E3B\",\n  \"tfgeMlMin\": 45,\n  \"tieneDM\": false,\n  \"tieneHTA\": true,\n  \"paSistolica\": 148,\n  \"paDiastolica\": 88,\n  \"ldl\": 135,\n  \"hdl\": 42,\n  \"tg\": 210,\n  \"glicemia\": 98,\n  \"hba1c\": 6.4,\n  \"racMgG\": 28,\n  \"imc\": 29.5,\n  \"circAbdomenCm\": 98,\n  \"fechaActual\": \"2025-08-10\"\n}"
    output_json: str = ""
    error: str | None = None

    def procesar(self):
        try:
            data = json.loads(self.input_json)
        except json.JSONDecodeError as e:
            self.error = f"JSON inválido: {e}"
            return
        resultado = procesar_json(data)
        if "error" in resultado:
            self.error = "Error de validación"
        else:
            self.error = None
        self.output_json = json.dumps(resultado, indent=2, ensure_ascii=False)


def cardiaia_page():
    return rx.box(
        rx.vstack(
            rx.heading("CardiaIA", size="4"),
            rx.text("Pega/edita JSON paciente"),
            rx.hstack(
                rx.text_area(
                    value=CardiaState.input_json,
                    on_change=CardiaState.set_input_json,
                    width="50%",
                    height="500px",
                ),
                rx.vstack(
                    rx.button("Procesar", on_click=CardiaState.procesar),
                    rx.cond(
                        CardiaState.error.is_not_none(),
                        rx.text(CardiaState.error, color="red"),
                    ),
                    rx.text_area(
                        value=CardiaState.output_json,
                        width="100%",
                        height="460px",
                        is_read_only=True,
                    ),
                    width="50%",
                    padding="1rem",
                ),
            ),
            padding="1rem",
        ),
        rx.link(
            "Ver HTML Legacy",
            href="/legacy/cardiaia.html",
            underline="always",
        ),
        width="100%",
    )


def get_page():
    return cardiaia_page()


__all__ = ["get_page", "cardiaia_page", "CardiaState"]
