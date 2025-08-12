"""Estado central de la aplicación Reflex (esqueleto inicial PR1).

Este módulo define la clase AppState que mantendrá:
- Datos del paciente
- Lista de laboratorios cargados / normalizados
- Medicamentos actuales
- Cálculos derivados (riesgo CV, TFG, fragilidad, etc.)

Iteración PR1: solo placeholders y estructura; lógica se llenará en PRs posteriores.
"""
from __future__ import annotations
from typing import List, Optional, Dict
import reflex as rx

from rcvco.ui.types import Programa
from rcvco.ui.calculos import (
    calc_imc,
    calc_tfg_cg,
    get_estadio_erc,
    calc_riesgo_cv_4_pasos,
    get_metas_programa,
)
from rcvco.ui.catalogs import (
    FACTORES_RIESGO,
    POTENCIADORES_RIESGO,
    LABS_MAP,
)

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
    # Datos básicos
    paciente_nombre: str = ""
    paciente_edad: int | None = None
    paciente_sexo: str = ""  # 'M' / 'F'
    paciente_peso_kg: float | None = None
    paciente_talla_m: float | None = None
    
    # Enfermedades base
    dx_dm: bool = False  # Diabetes mellitus
    dx_hta: bool = False  # Hipertensión arterial
    dx_erc: bool = False  # Enfermedad renal
    dx_cardiovascular: bool = False  # ECV establecida

    # Laboratorios y medicamentos
    labs: List[LabItem] = []
    medicamentos: List[MedicamentoItem] = []

    # Edición medicamento
    med_edit_nombre: str = ""
    med_edit_dosis: str = ""
    med_edit_frecuencia: str = "" 
    med_edit_idx: int | None = None

    # Fragilidad Fried
    perdida_peso: bool = False
    agotamiento: bool = False
    debilidad: bool = False
    lentitud: bool = False
    inactividad: bool = False

    # Cálculos derivados
    riesgo_cv_categoria: str = ""  # Muy alto/Alto/Moderado/Bajo
    riesgo_justificacion: str = ""  # Explicación sin mencionar "pasos"
    tfg_cg: float | None = None  # TFG Cockcroft-Gault
    imc: float | None = None
    es_fragil: bool = False  # ≥3 criterios Fried

    # Metas terapéuticas
    meta_pa_sys: int = 130  # sistólica objetivo
    meta_pa_dia: int = 80   # diastólica objetivo
    meta_ldl: int = 70      # mg/dL objetivo
    meta_hba1c: float = 7.0 # % objetivo (ajustable)

    # Estado PA actual
    pa_sistolica: str = ""
    pa_diastolica: str = ""
    
    # Próximos labs (fechas ISO)
    proximo_labs: Dict[str, str] = {}  # nombre_lab -> YYYY-MM-DD

    # Factores y potenciadores de riesgo
    factores_riesgo: List[str] = []
    potenciadores: List[str] = []

    # Estado edición lab
    lab_edit_nombre: str = ""
    lab_edit_valor: float | None = None
    lab_edit_fecha: str = ""
    lab_edit_idx: int | None = None

    # Estado informe
    informe_html: str = ""
    informe_pdf_url: str = ""

    # Flags UI modales
    modal_labs_abierto: bool = False
    modal_meds_abierto: bool = False
    modal_fragilidad_abierto: bool = False
    modal_labs_proximos_abierto: bool = False
    modal_informe_abierto: bool = False

    # Otros flags UI
    upload_error: str = ""
    generando_informe: bool = False
    dark_mode: bool = False  # soporte tema oscuro

    # Computed flags
    @rx.var
    def pa_control_ok(self) -> bool:
        """Verifica si PA está en meta."""
        try:
            sys = float(self.pa_sistolica or "0")
            dia = float(self.pa_diastolica or "0")
            return sys <= self.meta_pa_sys and dia <= self.meta_pa_dia
        except ValueError:
            return False

    @rx.var
    def ldl_control_ok(self) -> bool:
        """Verifica si LDL está en meta."""
        ldl = next((lab.valor for lab in self.labs if lab.nombre == "COLESTEROL LDL"), None)
        return bool(ldl and ldl <= self.meta_ldl)

    # Setters básicos
    def set_paciente_nombre(self, v: str):
        self.paciente_nombre = v

    def set_paciente_edad(self, v: int):
        self.paciente_edad = v
        self._recalc_all()

    def set_paciente_sexo(self, v: str):
        self.paciente_sexo = v
        self._recalc_all()

    def set_paciente_peso_kg(self, v: float):
        self.paciente_peso_kg = v
        self._recalc_all()

    def set_paciente_talla_m(self, v: float):
        self.paciente_talla_m = v
        self._recalc_all()

    def set_dx_dm(self, v: bool):
        self.dx_dm = v
        self._recalc_all()

    def set_dx_hta(self, v: bool):
        self.dx_hta = v
        self._recalc_all()

    def set_dx_erc(self, v: bool):
        self.dx_erc = v
        self._recalc_all()

    def set_dx_cardiovascular(self, v: bool):
        self.dx_cardiovascular = v
        self._recalc_all()

    # Setters fragilidad
    def set_perdida_peso(self, v: bool):
        self.perdida_peso = v
        self._recalc_fragilidad()

    def set_agotamiento(self, v: bool):
        self.agotamiento = v
        self._recalc_fragilidad()
        
    def set_debilidad(self, v: bool):
        self.debilidad = v
        self._recalc_fragilidad()

    def set_lentitud(self, v: bool):
        self.lentitud = v
        self._recalc_fragilidad()

    def set_inactividad(self, v: bool):
        self.inactividad = v
        self._recalc_fragilidad()

    # Gestión medicamentos
    def edit_medicamento(self, item: MedicamentoItem):
        """Abre modal edición medicamento."""
        self.med_edit_nombre = item.nombre
        self.med_edit_dosis = item.dosis or ""
        self.med_edit_frecuencia = item.frecuencia or ""
        self.med_edit_idx = next(
            (i for i, m in enumerate(self.medicamentos) if m == item),
            None
        )
        self.modal_meds_abierto = True

    def remove_medicamento(self, item: MedicamentoItem):
        """Elimina medicamento de la lista."""
        self.medicamentos = [m for m in self.medicamentos if m != item]

    def save_medicamento(self):
        """Guarda cambios medicamento."""
        if not self.med_edit_nombre:
            return
        
        med = MedicamentoItem(
            nombre=self.med_edit_nombre,
            dosis=self.med_edit_dosis,
            frecuencia=self.med_edit_frecuencia
        )

        if self.med_edit_idx is not None:
            self.medicamentos[self.med_edit_idx] = med
        else:
            self.medicamentos.append(med)

        self.med_edit_nombre = ""
        self.med_edit_dosis = ""
        self.med_edit_frecuencia = ""
        self.med_edit_idx = None
        self.modal_meds_abierto = False
        
    # Handlers laboratorios
    def set_lab_edit_nombre(self, v: str):
        """Actualiza nombre lab en edición."""
        self.lab_edit_nombre = v

    def set_lab_edit_valor(self, v: float):
        """Actualiza valor lab en edición."""
        self.lab_edit_valor = v
        
    def set_lab_edit_fecha(self, v: str):
        """Actualiza fecha lab en edición."""
        self.lab_edit_fecha = v

    def edit_lab(self, item: LabItem):
        """Abre modal edición lab."""
        self.lab_edit_nombre = item.nombre
        self.lab_edit_valor = item.valor
        self.lab_edit_fecha = item.fecha or ""
        self.lab_edit_idx = next(
            (i for i, lab in enumerate(self.labs) if lab == item),
            None
        )
        self.modal_labs_abierto = True

    def save_lab(self):
        """Guarda cambios laboratorio."""
        if not all([
            self.lab_edit_nombre,
            self.lab_edit_valor is not None,
            self.lab_edit_fecha
        ]):
            return

        lab = LabItem(
            nombre=self.lab_edit_nombre,
            valor=self.lab_edit_valor,
            unidad=LABS_MAP[self.lab_edit_nombre],
            fecha=self.lab_edit_fecha,
        )

        if self.lab_edit_idx is not None:
            self.labs[self.lab_edit_idx] = lab
        else:
            self.labs.append(lab)

        self.lab_edit_nombre = ""
        self.lab_edit_valor = None
        self.lab_edit_fecha = ""
        self.lab_edit_idx = None
        self.modal_labs_abierto = False
        self._recalc_all()

    # Toggle modales
    def toggle_modal_labs(self):
        """Toggle modal laboratorios."""
        self.modal_labs_abierto = not self.modal_labs_abierto
        if not self.modal_labs_abierto:
            self.lab_edit_nombre = ""
            self.lab_edit_valor = None
            self.lab_edit_fecha = ""
            self.lab_edit_idx = None

    def toggle_modal_fragilidad(self):
        """Toggle modal fragilidad."""
        self.modal_fragilidad_abierto = not self.modal_fragilidad_abierto

    def toggle_modal_labs_proximos(self):
        """Toggle modal próximos labs."""
        self.modal_labs_proximos_abierto = not self.modal_labs_proximos_abierto
        
    def toggle_modal_informe(self):
        """Toggle modal informe."""
        self.modal_informe_abierto = not self.modal_informe_abierto
        if not self.modal_informe_abierto:
            self.informe_html = ""
            self.informe_pdf_url = ""
        
    # Laboratorios
    def edit_lab(self, item: LabItem):
        """Abre modal edición laboratorio."""
        pass # TODO: Implementar en PR2
        
    # Recálculos internos
    def _recalc_all(self):
        """Recalcula todos los valores derivados."""
        if not all([
            self.paciente_edad,
            self.paciente_peso_kg,
            self.paciente_talla_m,
            self.paciente_sexo
        ]):
            return

        # 1. IMC
        self.imc = calc_imc(
            peso_kg=self.paciente_peso_kg,
            talla_m=self.paciente_talla_m,
        )

        # 2. TFG (requiere creatinina)
        creatinina = next(
            (lab.valor for lab in self.labs 
             if lab.nombre == "CREATININA EN SUERO U OTROS"),
            None
        )
        if creatinina:
            self.tfg_cg = calc_tfg_cg(
                edad=self.paciente_edad,
                peso_kg=self.paciente_peso_kg,
                creatinina_mg_dl=creatinina,
                sexo=self.paciente_sexo,
            )
            
            # 3. Estadio para metas
            estadio = get_estadio_erc(self.tfg_cg)
        else:
            self.tfg_cg = None
            estadio = None

        # 4. Riesgo CV
        ldl = next(
            (lab.valor for lab in self.labs 
             if lab.nombre == "COLESTEROL LDL"),
            None
        )
        try:
            pas = float(self.pa_sistolica) if self.pa_sistolica else None
        except ValueError:
            pas = None
            
        nivel, justificacion = calc_riesgo_cv_4_pasos(
            edad=self.paciente_edad,
            sexo=self.paciente_sexo,
            has_ecv=self.dx_cardiovascular,
            has_dm=self.dx_dm,
            has_hta=self.dx_hta,
            tfg=self.tfg_cg,
            pa_sistolica=pas,
            ldl=ldl,
            factores_riesgo=[
                f for f in self.factores_riesgo
                if f in FACTORES_RIESGO
            ],
            potenciadores=[
                p for p in self.potenciadores
                if p in POTENCIADORES_RIESGO
            ],
        )
        self.riesgo_cv_categoria = nivel
        self.riesgo_justificacion = justificacion

        # 5. Metas por programa prioritario
        if self.dx_erc:
            programa = Programa.ERC
        elif self.dx_dm:
            programa = Programa.DM
        elif self.dx_hta:
            programa = Programa.HTA
        else:
            return
            
        self.meta_pa_sys, self.meta_pa_dia, self.meta_ldl, self.meta_hba1c = get_metas_programa(
            programa=programa,
            edad=self.paciente_edad,
            has_ecv=self.dx_cardiovascular,
            estadio=estadio,
        )

        # 6. Estado fragilidad
        self._recalc_fragilidad()

    def _recalc_fragilidad(self):
        """Recalcula estado fragilidad."""
        criterios = sum([
            self.perdida_peso,
            self.agotamiento,
            self.debilidad,
            self.lentitud,
            self.inactividad
        ])
        self.es_fragil = criterios >= 3

    def toggle_modal_labs(self):
        self.modal_labs_abierto = not self.modal_labs_abierto

    def toggle_modal_meds(self):
        self.modal_meds_abierto = not self.modal_meds_abierto

__all__ = ["AppState", "LabItem", "MedicamentoItem"]
