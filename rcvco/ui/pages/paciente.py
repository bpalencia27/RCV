import reflex as rx
from rcvco.domain.models import Paciente, ResumenRiesgo
from rcvco.domain.labs import agenda_labs
from rcvco.domain.scoring import calcula_puntaje
from rcvco.domain.risk import clasificar_riesgo_cv_4_pasos, ascvd_ajustado
from rcvco.domain.tfg import crcl_cockcroft_gault
from rcvco.domain.report import generar_informe


class AppState(rx.State):
    paciente: Paciente | None = None
    resumen: ResumenRiesgo | None = None
    informe: str = ""

    # Campos formulario
    sexo: str = "M"
    edad: str = "60"
    peso: str = "80.0"
    has_dm: bool = False
    has_hta: bool = True
    estadio_erc: str = "3"

    def set_edad(self, value: str):
        if value.strip():
            self.edad = value

    def set_peso(self, value: str):
        if value.strip():
            self.peso = value

    def set_estadio_erc(self, value: str):
        if value.strip():
            self.estadio_erc = value

    def cargar_demo(self):
        from datetime import date
        from rcvco.domain.models import LabResult

        try:
            edad = int(self.edad)
            peso = float(self.peso)
            estadio_erc = int(self.estadio_erc) if self.estadio_erc.strip() else None
        except (ValueError, TypeError):
            return

        self.paciente = Paciente(
            pseudo_id="demo",
            sexo=self.sexo,
            edad=edad,
            peso_kg=peso,
            has_dm=self.has_dm,
            has_hta=self.has_hta,
            estadio_erc=estadio_erc,
            labs=[
                LabResult(
                    nombre="CREATININA EN SUERO U OTROS",
                    valor=1.1,
                    unidad="mg/dL",
                    fecha=date(2025, 5, 1),
                ),
                LabResult(
                    nombre="HEMOGLOBINA GLICOSILADA (HBA1C)",
                    valor=7.2,
                    unidad="%",
                    fecha=date(2025, 4, 15),
                ),
                LabResult(
                    nombre="COLESTEROL LDL",
                    valor=145,
                    unidad="mg/dL",
                    fecha=date(2025, 3, 20),
                ),
                LabResult(
                    nombre="PRESION ARTERIAL SISTOLICA",
                    valor=150,
                    unidad="mmHg",
                    fecha=date(2025, 6, 1),
                ),
            ],
        )
        self._recalcular()

    def _recalcular(self):
        if not self.paciente:
            return
        agenda = agenda_labs(self.paciente)
        puntaje = calcula_puntaje(self.paciente)
        riesgo = clasificar_riesgo_cv_4_pasos(self.paciente)
        ascvd = ascvd_ajustado(self.paciente)
        crcl = crcl_cockcroft_gault(self.paciente)
        self.resumen = ResumenRiesgo(
            riesgo_categoria=riesgo,
            puntaje=puntaje,
            ascvd=ascvd,
            aclaramiento_creatinina=crcl,
            agenda=agenda,
        )
        self.informe = generar_informe(self.paciente, self.resumen).texto


def badge(texto: str, color: str = "blue"):
    return rx.box(texto, bg_color=color, padding="0.5rem", border_radius="md")


def agenda_table(agenda):
    return rx.cond(
        agenda.is_none(),
        rx.text("Sin agenda."),
        rx.vstack(
            rx.hstack(
                rx.box("Examen", bg="gray.100", padding="0.5rem", width="25%"),
                rx.box("Fecha", bg="gray.100", padding="0.5rem", width="25%"),
                rx.box("Revisión", bg="gray.100", padding="0.5rem", width="25%"),
                rx.box("Motivo", bg="gray.100", padding="0.5rem", width="25%"),
                width="100%",
            ),
            rx.foreach(
                agenda,
                lambda item: rx.hstack(
                    rx.box(str(item.examen), padding="0.5rem", width="25%"),
                    rx.box(str(item.fecha_programada), padding="0.5rem", width="25%"),
                    rx.box(f"Revisión: {str(item.revision_fecha)}", padding="0.5rem", width="25%"),
                    rx.box(str(item.motivo), padding="0.5rem", width="25%"),
                    width="100%",
                ),
            ),
            width="100%",
            border="1px solid",
            border_color="gray.200",
            border_radius="md",
        ),
    )


def _form():
    return rx.box(
        rx.vstack(
            rx.heading("Datos Paciente", size="4"),
            rx.hstack(
                rx.select(
                    ["M", "F"],
                    value=AppState.sexo,
                    on_change=AppState.set_sexo,
                ),
                rx.input(
                    type="number",
                    value=AppState.edad,
                    on_change=AppState.set_edad,
                    placeholder="Edad",
                ),
                rx.input(
                    type="number",
                    value=AppState.peso,
                    on_change=AppState.set_peso,
                    placeholder="Peso (kg)",
                ),
                rx.switch(
                    is_checked=AppState.has_dm,
                    on_change=AppState.set_has_dm,
                    label="DM",
                ),
                rx.switch(
                    is_checked=AppState.has_hta,
                    on_change=AppState.set_has_hta,
                    label="HTA",
                ),
                rx.input(
                    type="number",
                    placeholder="Estadio ERC",
                    value=AppState.estadio_erc,
                    on_change=AppState.set_estadio_erc,
                    width="110px",
                ),
                spacing="4",
                padding="1rem",
            ),
            rx.button(
                "Cargar Ejemplo",
                on_click=AppState.cargar_demo,
            ),
            spacing="4",
            padding="1rem",
            width="100%",
        ),
        width="100%",
    )


def page():
    return rx.box(
        rx.vstack(
            rx.heading("Evaluación Paciente", size="4"),
            _form(),
            rx.cond(
                AppState.resumen.is_none(),
                rx.text("Pulse 'Cargar Ejemplo' o complete datos."),
            ),
            rx.cond(
                ~AppState.resumen.is_none(),
                rx.vstack(
                    rx.hstack(
                        rx.text(f"Riesgo: {AppState.resumen.riesgo_categoria}"),
                        rx.text(f"Puntaje: {AppState.resumen.puntaje}"),
                        rx.text(f"ASCVD: {AppState.resumen.ascvd:.1f}%"),
                        rx.text(f"CrCl: {AppState.resumen.aclaramiento_creatinina} ml/min"),
                    ),
                    rx.box(
                        rx.heading("Agenda de Laboratorios", size="4"),
                        agenda_table(AppState.resumen.agenda),
                        padding="1rem",
                    ),
                    rx.box(
                        rx.heading("Informe", size="4"),
                        rx.text_area(
                            value=AppState.informe,
                            width="100%",
                            height="180px",
                            is_read_only=True,
                        ),
                        padding="1rem",
                    ),
                    width="100%",
                    padding="1rem",
                ),
            ),
            width="100%",
            padding="1rem",
        ),
        width="100%",
    )


def get_page():
    return page()

__all__ = ["get_page", "page", "AppState"]
