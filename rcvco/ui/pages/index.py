"""Página index avanzada adaptada del diseño CardiaIA (versión simplificada Reflex).

Se replica estructura principal (panel formulario + panel informe) usando Tailwind.
Se implementa lógica básica en estado Reflex para:
 - Cálculo IMC
 - Cálculo TFG (Cockcroft-Gault simplificada)
 - Clasificación de riesgo simple (basada en diagnósticos, TFG, edad)
 - Generación de informe usando servicio LLM existente si disponible

Limitaciones iniciales (próximos pasos):
 - Gráficas (Chart.js) no implementadas todavía
 - Carga / parsing de PDF y extracción con IA se omite (reemplazable por endpoint futuro)
 - Historial local se simplifica (pendiente persistencia localStorage -> Reflex storage)
 - Metas dinámicas parciales
"""
from __future__ import annotations
import reflex as rx
from typing import List, Optional
from rcvco.services.report_service import build_prompt
from rcvco.ui.calculos import calc_imc, calc_tfg, calc_riesgo
import logging, sys

# Configuración básica de logging (si ya existe otra, se puede ajustar)
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
logger = logging.getLogger("rcvco.ui")
from rcvco.ui.theme import theme


class IndexState(rx.State):
    # Datos paciente
    nombre: str = ""
    edad: str = ""  # mantener como str para entrada
    sexo: str = "m"  # 'm'/'f'
    peso: str = ""   # kg
    talla: str = ""  # cm
    per_abd: str = ""  # perímetro abdominal

    # Diagnósticos principales
    dx_hta: bool = False
    dx_dm: bool = False
    dx_erc: bool = False

    # Condiciones adicionales
    ecv_establecida: bool = False
    tabaquismo: bool = False
    cond_socioeconomicas: bool = False
    fragil: bool = False

    # Adherencia / acceso
    adherencia: str = "buena"
    barreras_acceso: bool = False

    # Laboratorios clave (inputs manuales simplificados)
    creatinina: str = ""
    creatinina_date: str = ""
    ldl: str = ""
    hba1c: str = ""
    rac: str = ""  # relación alb/creat

    # Dinámicos calculados
    imc_display: str = ""
    tfg_display: str = ""
    riesgo_nivel: str = "INCOMPLETO"
    riesgo_factores: List[str] = []

    # Informe generado
    generando: bool = False
    informe_html: str = ""

    # Medicamentos simples (nombre, dosis, frecuencia)
    medicamentos: List[tuple[str, str, str]] = []
    # Laboratorios estructurados (id, label, valor, fecha) listado tipado
    labs_registrados: List[dict] = []  # lista simple; adaptamos foreach usando map helper

    @rx.var
    def labs_strings(self) -> List[str]:  # type: ignore[override]
        res: List[str] = []
        for lab in self.labs_registrados:
            label = str(lab.get("label", ""))
            valor = lab.get("valor", "")
            fecha = lab.get("fecha", "") or ""
            s = f"{label}: {valor}"
            if fecha:
                s += f" ({fecha})"
            res.append(s)
        return res

    @rx.var
    def pa_control_ok(self) -> bool:  # type: ignore[override]
        try:
            if not self.pa_sistolica or not self.pa_diastolica:
                return False
            return int(self.pa_sistolica) < self.meta_pa_sys
        except Exception:
            return False

    @rx.var
    def ldl_control_ok(self) -> bool:  # type: ignore[override]
        for lab in self.labs_registrados:
            if lab.get("id") == "ldl":
                try:
                    return float(lab.get("valor")) < self.meta_ldl
                except Exception:
                    return False
        return False

    @rx.var
    def hba1c_control_ok(self) -> bool:  # type: ignore[override]
        for lab in self.labs_registrados:
            if lab.get("id") == "hba1c":
                try:
                    return float(lab.get("valor")) < self.meta_hba1c
                except Exception:
                    return False
        return False

    @rx.var
    def has_chart_labs(self) -> bool:  # type: ignore[override]
        return any(l.get("id") in {"ldl", "hba1c"} for l in self.labs_registrados)

    @rx.var
    def chart_script(self) -> str:  # type: ignore[override]
        # Genera script Chart.js simple a partir de labs
        labs = [l for l in self.labs_registrados if l.get("id") in {"ldl", "hba1c"}]
        if not labs:
            return ""
        import json
        datasets = []
        for metric, label, color in [("ldl", "LDL", "#364FC7"), ("hba1c", "HbA1c", "#f59e0b")]:
            pts = [
                {"x": l.get("fecha") or "", "y": l.get("valor")}
                for l in labs if l.get("id") == metric
            ]
            if pts:
                datasets.append({"label": label, "data": pts, "borderColor": color, "backgroundColor": color + "33", "fill": False})
        return (
            "<script src=\"https://cdn.jsdelivr.net/npm/chart.js\"></script><script>"+
            "(function(){const el=document.getElementById('chart-trends');if(!el)return;"+
            "if(window.__trendChart__){window.__trendChart__.destroy();}"+
            f"const data={{datasets:{json.dumps(datasets)}}};"+
            "window.__trendChart__=new Chart(el.getContext('2d'),{type:'line',data:data,options:{responsive:true,parsing:false,scales:{x:{display:false}}}});})();"+
            "</script>"
        )

    # Historial pacientes (solo nombres + snapshot reducido)
    historial: List[dict] = []

    # Modales / UI flags
    modal_fragilidad: bool = False
    modal_historial: bool = False
    modal_alerta: bool = False
    alerta_titulo: str = ""
    alerta_mensaje: str = ""
    high_contrast: bool = False
    dark_mode: bool = False

    # Fragilidad (criterios Fried)
    fried_perdida_peso: bool = False
    fried_agotamiento: bool = False
    fried_actividad_baja: bool = False
    fried_lentitud: bool = False
    fried_debilidad: bool = False

    # Metas calculadas
    meta_pa_sys: int = 130
    meta_pa_dia: int = 80
    meta_ldl: int = 70
    meta_hba1c: float = 7.0

    pa_sistolica: str = ""  # para metas rápidas (primer valor)
    pa_diastolica: str = ""

    # Campos laboratorio manual dinámico soporte toggle
    mostrar_labs_manual: bool = False
    # Texto bruto de laboratorio y estado de parseo
    lab_text_raw: str = ""
    parsing: bool = False
    parse_error: str = ""

    # Estado charts (se fuerza un contador para regenerar script)
    charts_version: int = 0
    # Subida archivo
    upload_error: str = ""
    upload_name: str = ""

    async def subir_archivo(self, file: rx.UploadFile):  # type: ignore[override]
        self.upload_error = ""
        try:
            import httpx, json
            content = await file.read()
            # Enviar como multipart
            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.post(
                    "/api/upload",
                    files={"file": (file.filename, content, file.content_type or "application/octet-stream")},
                )
            if resp.status_code != 200:
                raise RuntimeError(f"HTTP {resp.status_code}")
            data = resp.json()
            self.upload_name = file.filename
            # Agregar labs si vienen
            for l in data.get("labs", []):
                nombre = l.get("nombre")
                valor = l.get("valor")
                if nombre and valor is not None:
                    mapping = {
                        "CREATININA EN SUERO U OTROS": ("creat", "Creatinina"),
                        "HEMOGLOBINA GLICOSILADA (HBA1C)": ("hba1c", "HbA1c (%)"),
                        "COLESTEROL LDL": ("ldl", "Colesterol LDL (mg/dL)"),
                    }
                    if nombre in mapping:
                        lab_id, label = mapping[nombre]
                        self.upsert_lab(lab_id, label, str(valor), "")
        except Exception as e:  # noqa: BLE001
            self.upload_error = str(e)[:140]

    def add_medicamento(self):
        self.medicamentos.append(("", "", ""))

    # --- Setters básicos ---
    def set_nombre(self, v: str):
        self.nombre = v

    def set_edad(self, v: str):
        self.edad = v

    def set_sexo(self, v: str):
        self.sexo = v

    def set_peso(self, v: str):
        self.peso = v

    def set_talla(self, v: str):
        self.talla = v

    def set_dx_hta(self, v: bool):
        self.dx_hta = v

    def set_dx_dm(self, v: bool):
        self.dx_dm = v

    def set_dx_erc(self, v: bool):
        self.dx_erc = v

    def set_ecv_establecida(self, v: bool):
        self.ecv_establecida = v

    def set_tabaquismo(self, v: bool):
        self.tabaquismo = v

    def set_cond_socioeconomicas(self, v: bool):
        self.cond_socioeconomicas = v

    def set_creatinina(self, v: str):
        self.creatinina = v

    def set_creatinina_date(self, v: str):
        self.creatinina_date = v

    def set_ldl(self, v: str):
        self.ldl = v

    def set_hba1c(self, v: str):
        self.hba1c = v

    def set_rac(self, v: str):
        self.rac = v

    def set_adherencia(self, v: str):
        self.adherencia = v

    def set_barreras_acceso(self, v: bool):
        self.barreras_acceso = v

    def set_lab_text_raw(self, v: str):
        self.lab_text_raw = v

    def toggle_labs_manual(self, v: bool):
        self.mostrar_labs_manual = v

    # Medicamentos helpers
    def set_med_nombre(self, i: int, v: str):
        if 0 <= i < len(self.medicamentos):
            n, d, f = self.medicamentos[i]
            self.medicamentos[i] = (v, d, f)

    def set_med_dosis(self, i: int, v: str):
        if 0 <= i < len(self.medicamentos):
            n, d, f = self.medicamentos[i]
            self.medicamentos[i] = (n, v, f)

    def set_med_freq(self, i: int, v: str):
        if 0 <= i < len(self.medicamentos):
            n, d, f = self.medicamentos[i]
            self.medicamentos[i] = (n, d, v)

    def remove_medicamento(self, i: int):
        if 0 <= i < len(self.medicamentos):
            removed = self.medicamentos.pop(i)
            logger.info(f"Medicamento eliminado index={i} valor={removed}")
        else:
            logger.warning(f"remove_medicamento índice inválido={i} total={len(self.medicamentos)}")

    # Labs helper
    def upsert_lab(self, lab_id: str, label: str, valor: str, fecha: str):
        for lab in self.labs_registrados:
            if lab.get("id") == lab_id:
                if valor:
                    lab["valor"] = valor
                if fecha:
                    lab["fecha"] = fecha
                lab["label"] = label or lab.get("label", "")
                break
        else:
            self.labs_registrados.append({"id": lab_id, "label": label, "valor": valor, "fecha": fecha})

    def _calc_imc(self):
        self.imc_display = calc_imc(self.peso, self.talla)
    def set_pa_diastolica(self, v: str):
        self.pa_diastolica = v
        self.recompute()

    def set_pa_sistolica(self, v: str):
        self.pa_sistolica = v
        self.recompute()

    # --- Fragilidad ---
    def set_fried(self, campo: str, value: bool):
        setattr(self, campo, value)
        self._calc_fragilidad()
        # Actualizar el resto del estado (sin entrar en recursión)
        self._calc_imc()
        self._calc_tfg()
        self._calc_riesgo()

    def _calc_fragilidad(self):
        criterios = [
            self.fried_perdida_peso,
            self.fried_agotamiento,
            self.fried_actividad_baja,
            self.fried_lentitud,
            self.fried_debilidad,
        ]
        cnt = sum(1 for c in criterios if c)
        self.fragil = cnt >= 3

    # --- Historial ---
    def guardar_en_historial(self):
        snap = {
            "nombre": self.nombre or "PACIENTE",
            "edad": self.edad,
            "riesgo": self.riesgo_nivel,
            "tfg": self.tfg_display,
            "fecha_creat": self.creatinina_date,
        }
        self.historial = [h for h in self.historial if h["nombre"] != snap["nombre"]]
        self.historial.insert(0, snap)
        self.alerta_titulo = "Guardado"
        self.alerta_mensaje = f"Paciente {snap['nombre']} almacenado en historial."
        self.modal_alerta = True

    def cargar_historial(self, idx: int):
        try:
            if 0 <= idx < len(self.historial):
                h = self.historial[idx]
                logger.info(f"Cargando historial idx={idx} nombre={h.get('nombre')}")
                self.nombre = h.get("nombre", "")
                self.edad = h.get("edad", "")
                self.recompute()
                self.modal_historial = False
            else:
                logger.warning(f"cargar_historial índice fuera de rango idx={idx} total={len(self.historial)}")
        except Exception as e:  # noqa: BLE001
            logger.exception(f"Error al cargar historial idx={idx}: {e}")
            self.alerta_titulo = "Error"
            self.alerta_mensaje = "No se pudo cargar historial." 
            self.modal_alerta = True

    def cerrar_historial_modal(self):
        self.modal_historial = False

    # --- Alertas ---
    def cerrar_alerta(self):
        self.modal_alerta = False

    def cerrar_fragilidad_modal(self):
        self.modal_fragilidad = False

    # High contrast
    def toggle_contrast(self):
        self.high_contrast = not self.high_contrast

    def toggle_dark(self):
        self.dark_mode = not self.dark_mode

    def abrir_historial_modal(self):
        self.modal_historial = True

    def abrir_fragilidad_modal(self):
        self.modal_fragilidad = True

    # --- Cálculos (restaurados) ---
    def _calc_tfg(self):
        self.tfg_display = calc_tfg(self.edad, self.peso, self.creatinina, self.sexo)

    def _calc_riesgo(self):
        nivel, factores, meta_ldl = calc_riesgo(
            self.dx_dm,
            self.dx_hta,
            self.dx_erc,
            self.ecv_establecida,
            self.edad,
            self.tfg_display,
            self.rac,
            self.hba1c,
            self.ldl,
        )
        self.riesgo_nivel = nivel
        self.riesgo_factores = factores
        self.meta_ldl = meta_ldl

    def recompute(self):
        self._calc_imc()
        self._calc_tfg()
        self._calc_riesgo()
        # Ya no se llama a _calc_fragilidad aquí para evitar recursión infinita
        # Actualizar versión charts para re-render
        self.charts_version += 1

    # --- Parseo texto laboratorio ---
    async def parsear_texto(self):  # type: ignore[override]
        if not self.lab_text_raw.strip():
            self.parse_error = "Texto vacío"
            return
        self.parsing = True
        self.parse_error = ""
        try:
            try:
                import httpx
                async with httpx.AsyncClient(timeout=10.0) as client:
                        resp = await client.post("/api/parse-text", json={"raw": self.lab_text_raw}, headers={"Content-Type": "application/json"})
                if resp.status_code != 200:
                    raise RuntimeError(f"HTTP {resp.status_code}")
                data = resp.json()
            except Exception:
                # Fallback parser local (regex simple)
                import re
                txt = self.lab_text_raw.lower()
                pats = {
                    "CREATININA EN SUERO U OTROS": r"creatinina[^0-9]*([0-9]+\.?[0-9]*)",
                    "HEMOGLOBINA GLICOSILADA (HBA1C)": r"hba1c[^0-9]*([0-9]+\.?[0-9]*)",
                    "COLESTEROL LDL": r"ldl[^0-9]*([0-9]+\.?[0-9]*)",
                }
                labs_found = []
                for nombre, pat in pats.items():
                    m = re.search(pat, txt)
                    if m:
                        try:
                            labs_found.append({"nombre": nombre, "valor": float(m.group(1))})
                        except Exception:
                            pass
                data = {"labs": labs_found}
            # Integrar labs en labs_registrados
            for l in data.get("labs", []):
                nombre = l.get("nombre")
                valor = l.get("valor")
                if nombre and valor is not None:
                    # Map a id si coincide
                    mapping = {
                        "CREATININA EN SUERO U OTROS": ("creat", "Creatinina"),
                        "HEMOGLOBINA GLICOSILADA (HBA1C)": ("hba1c", "HbA1c (%)"),
                        "COLESTEROL LDL": ("ldl", "Colesterol LDL (mg/dL)"),
                    }
                    if nombre in mapping:
                        lab_id, label = mapping[nombre]
                        self.upsert_lab(lab_id, label, str(valor), "")
            self.lab_text_raw = ""
        except Exception as e:  # noqa: BLE001
            self.parse_error = f"Error parseo: {e}"[:140]
        finally:
            self.parsing = False

    # Evento principal: generar informe (usa servicio LLM si configurado)
    async def generar_informe(self):  # type: ignore[override]
        self.generando = True
        self.informe_html = ""
        # Construir payload simple alineado con build_prompt existente
        datos = {
            "pseudo_id": self.nombre or "PACIENTE",
            "sexo": self.sexo.upper(),
            "edad": int(self.edad) if self.edad.isdigit() else None,
            "peso_kg": float(self.peso) if self._is_float(self.peso) else None,
            "has_dm": self.dx_dm,
            "has_hta": self.dx_hta,
            "labs": [
                {"nombre": "CREATININA EN SUERO U OTROS", "valor": self._as_float(self.creatinina)},
                {"nombre": "HEMOGLOBINA GLICOSILADA (HBA1C)", "valor": self._as_float(self.hba1c)},
                {"nombre": "COLESTEROL LDL", "valor": self._as_float(self.ldl)},
            ],
            "medications": [
                {"nombre": n, "dosis": d, "freq": f}
                for (n, d, f) in self.medicamentos if n
            ],
        }
        datos["labs"] = [l for l in datos["labs"] if l["valor"] is not None]
        try:
            import httpx, html
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post("/api/preview-report", json=datos)
            if resp.status_code == 200:
                prompt = resp.json().get("prompt", "")
                self.informe_html = (
                    f"<h2>Informe Clínico (Borrador)</h2>"
                    f"<p><strong>Prompt Generado:</strong></p><pre style='white-space:pre-wrap;background:#f8fafc;padding:0.75rem;border-radius:0.5rem;'>{html.escape(prompt)}</pre>"
                    f"<p>Riesgo estimado: <strong>{self.riesgo_nivel}</strong></p>"
                )
            else:
                raise RuntimeError(f"preview-report HTTP {resp.status_code}")
        except Exception as e:  # noqa: BLE001
            logger.exception(f"Fallo generar_informe remoto: {e}; usando prompt local")
            import html
            prompt = build_prompt(datos)
            self.informe_html = (
                f"<h2>Informe Clínico (Borrador Local)</h2>"
                f"<pre style='white-space:pre-wrap;background:#f8fafc;padding:0.75rem;border-radius:0.5rem;'>{html.escape(prompt)}</pre>"
                f"<p>Riesgo estimado: <strong>{self.riesgo_nivel}</strong></p>"
            )
        finally:
            self.generando = False


def _risk_panel():
    return rx.box(
        rx.box(
            rx.text("Clasificación de Riesgo del Paciente", class_name="font-bold text-lg text-center text-gray-600 mb-3"),
            rx.box(IndexState.riesgo_nivel, class_name=_risk_level_class()),
            rx.box(
                rx.foreach(IndexState.riesgo_factores, lambda f: rx.text(f, class_name="flex items-center text-sm text-gray-600")),
                class_name="mt-4 space-y-1",
            ),
            class_name="p-5 rounded-xl mb-4 transition-all duration-500 bg-gray-200",
        ),
        class_name="w-full",
    )


# --- UI Helper Components (faltaban tras refactor) ---
def _section_title(text: str):
    return rx.heading(text, class_name="text-xl font-bold text-gray-700 border-b border-gray-200 pb-1")


def _input(label: str, value, type_: str = "text", required: bool = False, on_change=None):
    req = " <span class='text-red-500'>*</span>" if required else ""
    return rx.box(
        rx.html(f"<label class='font-medium text-sm mb-1 block'>{label}{req}</label>"),
        rx.input(value=value, type=type_, class_name="input-field", on_change=on_change, required=required),
    )


def _checkbox(label: str, checked, on_change=None, id_: str = ""):
    return rx.hstack(
        rx.checkbox(is_checked=checked, on_change=on_change, id=id_, class_name="h-5 w-5"),
        rx.text(label, class_name="content text-sm"),
        class_name="checkbox-card items-center",
    )


def _meds_list():
    return rx.vstack(
        rx.foreach(
            IndexState.medicamentos,
            lambda med, i: rx.hstack(
                rx.input(value=med[0], placeholder="Nombre", class_name="input-field", on_change=lambda v, i=i: IndexState.set_med_nombre(i, v)),
                rx.input(value=med[1], placeholder="Dosis", class_name="input-field", on_change=lambda v, i=i: IndexState.set_med_dosis(i, v)),
                rx.input(value=med[2], placeholder="Frecuencia", class_name="input-field", on_change=lambda v, i=i: IndexState.set_med_freq(i, v)),
                # Evitar que el parámetro evento (dict) sea interpretado como índice.
                rx.button("✕", on_click=lambda _=None, i=i: IndexState.remove_medicamento(i), class_name="text-red-500"),
                class_name="grid grid-cols-4 gap-2 w-full",
            ),
        ),
        rx.button("Añadir medicamento", on_click=IndexState.add_medicamento, class_name="text-sm font-medium text-primary mt-2"),
        class_name="space-y-2",
    )


def _labs_section():
    # Config labs manuales
    LABS = [
        ("hba1c", "HbA1c (%)"),
        ("ldl", "Colesterol LDL (mg/dL)"),
        ("hdl", "Colesterol HDL (mg/dL)"),
        ("rac", "RAC (mg/g)"),
        ("glicemia", "Glicemia (mg/dL)"),
        ("pth", "PTH (pg/mL)"),
        ("albumina", "Albúmina (g/dL)"),
    ]
    manual_inputs = rx.cond(
        IndexState.mostrar_labs_manual,
        rx.vstack(
            rx.foreach(
                LABS,
                lambda item: rx.hstack(
                    rx.text(item[1], class_name="font-medium text-sm w-2/5"),
                    rx.input(
                        placeholder="Valor",
                        class_name="input-field",
                        on_change=lambda v, lab_id=item[0], label=item[1]: IndexState.upsert_lab(lab_id, label, v, ""),
                    ),
                    rx.input(
                        type="date",
                        class_name="input-field",
                        on_change=lambda v, lab_id=item[0], label=item[1]: IndexState.upsert_lab(lab_id, label, "", v),
                    ),
                    class_name="w-full gap-2",
                ),
            ),
            class_name="space-y-2 mt-4",
        ),
        rx.box(),
    )
    listado = rx.vstack(
        rx.foreach(IndexState.labs_strings, lambda s: rx.box(s, class_name="text-sm bg-gray-50 p-2 rounded-md")),
    )
    return rx.box(
        rx.switch(
            is_checked=IndexState.mostrar_labs_manual,
            on_change=IndexState.toggle_labs_manual,
            label="Labs manuales",
        ),
        manual_inputs,
        listado,
        class_name="space-y-2",
    )


def _metas_panel():
    return rx.box(
        rx.heading("Metas Terapéuticas", class_name="font-bold text-lg text-center text-gray-600 mb-4"),
        rx.vstack(
            rx.hstack(
                rx.text("Presión Arterial", class_name="font-semibold text-sm w-1/3"),
                rx.text(f"Meta < {IndexState.meta_pa_sys}/{IndexState.meta_pa_dia}", class_name="text-xs text-gray-500 w-1/3"),
                rx.cond(IndexState.pa_control_ok, rx.text("✅", class_name="w-1/3 text-right"), rx.text("⚠", class_name="w-1/3 text-right")),
                class_name="w-full items-center",
            ),
            rx.hstack(
                rx.text("LDL", class_name="font-semibold text-sm w-1/3"),
                rx.text(f"Meta < {IndexState.meta_ldl} mg/dL", class_name="text-xs text-gray-500 w-1/3"),
                rx.cond(IndexState.ldl_control_ok, rx.text("✅", class_name="w-1/3 text-right"), rx.text("⚠", class_name="w-1/3 text-right")),
                class_name="w-full items-center",
            ),
            rx.hstack(
                rx.text("HbA1c", class_name="font-semibold text-sm w-1/3"),
                rx.text(f"Meta < {IndexState.meta_hba1c}%", class_name="text-xs text-gray-500 w-1/3"),
                rx.cond(IndexState.hba1c_control_ok, rx.text("✅", class_name="w-1/3 text-right"), rx.text("⚠", class_name="w-1/3 text-right")),
                class_name="w-full items-center",
            ),
            class_name="space-y-2",
        ),
        class_name="p-5 rounded-xl mb-6 bg-white shadow-sm",
    )


def _historial_modal():
    return rx.cond(
        IndexState.modal_historial,
        rx.box(
            rx.box(
                rx.heading("Historial Pacientes", size="5"),
                rx.vstack(
                    rx.foreach(
                        IndexState.historial,
                        lambda h, i: rx.hstack(
                            rx.text(f"{h['nombre']} (edad {h['edad']}) - {h['riesgo']}", class_name="text-sm"),
                            rx.button("Cargar", size="1", on_click=lambda _=None, i=i: IndexState.cargar_historial(i)),
                            spacing="2",
                            class_name="justify-between w-full bg-gray-50 p-2 rounded",
                        ),
                    ),
                    class_name="space-y-2 max-h-80 overflow-y-auto",
                ),
                rx.button("Cerrar", on_click=IndexState.cerrar_historial_modal, class_name="mt-4"),
                class_name="bg-white p-6 rounded-lg shadow-xl w-full max-w-md",
            ),
            class_name="fixed inset-0 flex items-center justify-center backdrop-blur-sm bg-black/40 z-50",
        ),
        rx.box(),
    )


def _fragilidad_modal():
    return rx.cond(
        IndexState.modal_fragilidad,
        rx.box(
            rx.box(
                rx.heading("Fragilidad (Fried)", size="5"),
                rx.vstack(
                    rx.hstack(
                        rx.checkbox(is_checked=IndexState.fried_perdida_peso, on_change=lambda v: IndexState.set_fried("fried_perdida_peso", v)),
                        rx.text("Pérdida de peso no intencionada", class_name="text-sm"),
                        class_name="items-center gap-2",
                    ),
                    rx.hstack(
                        rx.checkbox(is_checked=IndexState.fried_agotamiento, on_change=lambda v: IndexState.set_fried("fried_agotamiento", v)),
                        rx.text("Agotamiento", class_name="text-sm"),
                        class_name="items-center gap-2",
                    ),
                    rx.hstack(
                        rx.checkbox(is_checked=IndexState.fried_actividad_baja, on_change=lambda v: IndexState.set_fried("fried_actividad_baja", v)),
                        rx.text("Actividad física baja", class_name="text-sm"),
                        class_name="items-center gap-2",
                    ),
                    rx.hstack(
                        rx.checkbox(is_checked=IndexState.fried_lentitud, on_change=lambda v: IndexState.set_fried("fried_lentitud", v)),
                        rx.text("Lentitud marcha", class_name="text-sm"),
                        class_name="items-center gap-2",
                    ),
                    rx.hstack(
                        rx.checkbox(is_checked=IndexState.fried_debilidad, on_change=lambda v: IndexState.set_fried("fried_debilidad", v)),
                        rx.text("Debilidad (fuerza prensión)", class_name="text-sm"),
                        class_name="items-center gap-2",
                    ),
                    class_name="space-y-2 mt-4",
                ),
                rx.text(
                    rx.cond(IndexState.fragil, "Estado: Frágil", "Estado: No Frágil"),
                    class_name="mt-4 font-medium",
                ),
                rx.hstack(
                    rx.button("Cerrar", on_click=IndexState.cerrar_fragilidad_modal),
                    spacing="3",
                    class_name="mt-6 justify-end",
                ),
                class_name="bg-white p-6 rounded-lg shadow-xl w-full max-w-md",
            ),
            class_name="fixed inset-0 flex items-center justify-center backdrop-blur-sm bg-black/40 z-50",
        ),
        rx.box(),
    )


def _alerta_modal():
    return rx.cond(
        IndexState.modal_alerta,
        rx.box(
            rx.box(
                rx.heading(IndexState.alerta_titulo, size="5"),
                rx.text(IndexState.alerta_mensaje, class_name="text-sm mt-2"),
                rx.button("Cerrar", on_click=IndexState.cerrar_alerta, class_name="mt-4"),
                class_name="bg-white p-6 rounded-lg shadow-xl w-full max-w-sm",
            ),
            class_name="fixed inset-0 flex items-center justify-center backdrop-blur-sm bg-black/40 z-50",
        ),
        rx.box(),
    )


def _top_actions():
    return rx.hstack(
    rx.button("Historial", size="2", on_click=IndexState.abrir_historial_modal),
    rx.button("Fragilidad", size="2", on_click=IndexState.abrir_fragilidad_modal),
        rx.button(
            rx.cond(IndexState.high_contrast, "Contraste -", "Contraste +"),
            size="2",
            on_click=IndexState.toggle_contrast,
        ),
        rx.button(
            rx.cond(IndexState.dark_mode, "Claro", "Oscuro"),
            size="2",
            on_click=IndexState.toggle_dark,
        ),
        rx.button("Guardar Paciente", size="2", on_click=IndexState.guardar_en_historial),
        spacing="2",
        class_name="flex-wrap",
    )


def _parse_text_section():
    return rx.box(
        rx.heading("Importar Texto de Laboratorio", size="5", class_name="mb-2"),
        rx.text_area(
            value=IndexState.lab_text_raw,
            on_change=IndexState.set_lab_text_raw,
            placeholder="Pega aquí texto de un informe (contenga términos: creatinina, hba1c, ldl)...",
            height="120px",
            class_name="w-full input-field",
        ),
        rx.hstack(
            rx.button(
                rx.cond(IndexState.parsing, "Parseando...", "Parsear Texto"),
                on_click=IndexState.parsear_texto,
                disabled=IndexState.parsing,
            ),
            rx.cond(
                IndexState.parse_error != "",
                rx.text(IndexState.parse_error, color="red", class_name="text-sm"),
            ),
            spacing="3",
            class_name="mt-2",
        ),
        class_name="space-y-2 mt-6",
    )


def _upload_section():
    return rx.box(
        rx.heading("Subir Archivo (PDF/TXT)", size="5", class_name="mb-2"),
        rx.text("Placeholder: se procesa en backend parse_document"),
        rx.upload(
            rx.vstack(
                rx.text("Arrastra o haz click para seleccionar"),
                rx.text("Tipos: PDF, TXT", class_name="text-xs text-gray-500"),
                class_name="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center cursor-pointer hover:border-primary transition-colors"
            ),
            multiple=False,
            accept=".pdf,.txt",
            max_files=1,
        ),
        rx.text("(Procesamiento automático desactivado temporalmente: falta hook on_upload soportado en versión Reflex)", class_name="text-xs text-amber-600"),
    rx.cond(IndexState.upload_name != "", rx.text(IndexState.upload_name, class_name="text-sm mt-2")),
    rx.cond(IndexState.upload_error != "", rx.text(IndexState.upload_error, color="red", class_name="text-sm mt-2")),
        class_name="space-y-2 mt-6",
    )


def _charts_section():
    return rx.cond(
        IndexState.has_chart_labs,
        rx.box(
            rx.heading("Tendencias", size="5", class_name="mb-2"),
            rx.html('<canvas id="chart-trends" height="160"></canvas>'),
            rx.html(IndexState.chart_script),
            class_name="p-5 rounded-xl mb-6 bg-white shadow-sm",
        ),
        rx.box(),
    )


def _risk_level_class():
    # Devuelve clases según riesgo
    return rx.cond(
        IndexState.riesgo_nivel == "BAJO",
        "text-center font-extrabold text-3xl py-4 rounded-lg text-white bg-green-500",
        rx.cond(
            IndexState.riesgo_nivel == "MODERADO",
            "text-center font-extrabold text-3xl py-4 rounded-lg text-white bg-amber-500",
            rx.cond(
                IndexState.riesgo_nivel == "ALTO",
                "text-center font-extrabold text-3xl py-4 rounded-lg text-white bg-red-500",
                rx.cond(
                    IndexState.riesgo_nivel == "MUY ALTO",
                    "text-center font-extrabold text-3xl py-4 rounded-lg text-white bg-red-700",
                    "text-center font-extrabold text-3xl py-4 rounded-lg text-white bg-gray-400",
                ),
            ),
        ),
    )


def index_page():  # componente principal
    # Formulario (panel izquierdo)
    form_panel = rx.box(
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.html("""<svg class='w-10 h-10 text-primary' xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke-width='1.5' stroke='currentColor'><path stroke-linecap='round' stroke-linejoin='round' d='M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z' /></svg>"""),
                    rx.heading("CardiaIA", class_name="text-3xl font-extrabold text-gray-900"),
                    class_name="flex items-center gap-3 mb-2",
                ),
                rx.spacer(),
                class_name="justify-between items-center mb-6",
            ),
        ),
        rx.form(
            rx.vstack(
                _section_title("Datos del Paciente"),
                rx.grid(
                    _input("Nombre Completo", IndexState.nombre, required=True, on_change=[IndexState.set_nombre, IndexState.recompute]),
                    _input("Edad (años)", IndexState.edad, type_="number", required=True, on_change=[IndexState.set_edad, IndexState.recompute]),
                    rx.box(
                        rx.html("<label class='font-medium text-sm mb-1 block'>Sexo <span class='text-red-500'>*</span></label>"),
                        rx.select(["m", "f"], value=IndexState.sexo, on_change=[IndexState.set_sexo, IndexState.recompute], class_name="input-field"),
                    ),
                    _input("Peso (kg)", IndexState.peso, type_="number", required=True, on_change=[IndexState.set_peso, IndexState.recompute]),
                    _input("Talla (cm)", IndexState.talla, type_="number", on_change=[IndexState.set_talla, IndexState.recompute]),
                    rx.box(
                        rx.html("<label class='font-medium text-sm mb-1 block'>IMC</label>"),
                        rx.input(value=IndexState.imc_display, is_read_only=True, class_name="input-field bg-gray-100"),
                    ),
                    columns="2",
                    class_name="gap-x-6 gap-y-5",
                ),
                _section_title("Diagnósticos y Condiciones"),
                rx.grid(
                    _checkbox("Hipertensión (HTA)", IndexState.dx_hta, [IndexState.set_dx_hta, IndexState.recompute], "dx-hta"),
                    _checkbox("Diabetes (DM)", IndexState.dx_dm, [IndexState.set_dx_dm, IndexState.recompute], "dx-dm"),
                    _checkbox("ERC", IndexState.dx_erc, [IndexState.set_dx_erc, IndexState.recompute], "dx-erc"),
                    columns="3",
                    class_name="gap-3",
                ),
                rx.grid(
                    _checkbox("ECV establecida", IndexState.ecv_establecida, [IndexState.set_ecv_establecida, IndexState.recompute], "ecv"),
                    _checkbox("Tabaquismo", IndexState.tabaquismo, [IndexState.set_tabaquismo, IndexState.recompute], "tab"),
                    _checkbox("Cond. Socioeconómicas Adversas", IndexState.cond_socioeconomicas, [IndexState.set_cond_socioeconomicas, IndexState.recompute], "csa"),
                    columns="3",
                    class_name="gap-3",
                ),
                _section_title("Laboratorios"),
                rx.grid(
                    _input("Creatinina (mg/dL)", IndexState.creatinina, type_="number", required=True, on_change=[IndexState.set_creatinina, IndexState.recompute]),
                    _input("Fecha Creatinina", IndexState.creatinina_date, type_="date", on_change=[IndexState.set_creatinina_date, IndexState.recompute]),
                    _input("Colesterol LDL (mg/dL)", IndexState.ldl, type_="number", on_change=[IndexState.set_ldl, IndexState.recompute]),
                    _input("HbA1c (%)", IndexState.hba1c, type_="number", on_change=[IndexState.set_hba1c, IndexState.recompute]),
                    _input("RAC (mg/g)", IndexState.rac, type_="number", on_change=[IndexState.set_rac, IndexState.recompute]),
                    columns="2",
                    class_name="gap-x-6 gap-y-5",
                ),
                _labs_section(),
                _parse_text_section(),
                _upload_section(),
                _section_title("Tratamiento Farmacológico"),
                _meds_list(),
                _section_title("Adherencia y Acceso"),
                rx.grid(
                    rx.box(
                        rx.html("<label class='font-medium text-sm mb-1 block'>Adherencia al Tratamiento</label>"),
                        rx.select(["buena", "regular", "mala"], value=IndexState.adherencia, on_change=[IndexState.set_adherencia, IndexState.recompute], class_name="input-field"),
                    ),
                    _checkbox("Barreras de Acceso", IndexState.barreras_acceso, [IndexState.set_barreras_acceso, IndexState.recompute], "barr-acceso"),
                    columns="2",
                    class_name="gap-6",
                ),
                rx.button(
                    rx.cond(IndexState.generando, "Generando...", "Generar Informe Clínico"),
                    type_="button",
                    class_name="w-full bg-primary hover:bg-primary-light text-white font-bold py-3 rounded-lg",
                    on_click=[IndexState.recompute, IndexState.generar_informe],
                ),
                class_name="space-y-6",
            ),
            class_name="space-y-6 flex-grow overflow-y-auto",
        ),
        class_name="form-panel flex flex-col",
    )

    # Panel derecho (informe)
    report_panel = rx.box(
        _risk_panel(),
        _metas_panel(),
        _charts_section(),
        rx.box(
            rx.heading("Informe Clínico", class_name="text-2xl font-bold mb-4"),
            rx.cond(
                IndexState.informe_html == "",
                rx.text("El informe aparecerá aquí."),
                rx.html(IndexState.informe_html),
            ),
            class_name="p-5 rounded-xl bg-white shadow-sm",
        ),
        class_name="report-panel",
    )

    return rx.box(
        theme(),
        _alerta_modal(),
        _fragilidad_modal(),
        _historial_modal(),
        form_panel,
        report_panel,
        rx.box(_top_actions(), class_name="fixed bottom-4 left-1/2 -translate-x-1/2 flex gap-2 fixed-action-bar px-4 py-2 rounded-xl"),
        class_name=rx.cond(
            IndexState.high_contrast,
            rx.cond(IndexState.dark_mode, "main-grid high-contrast dark-mode", "main-grid high-contrast"),
            rx.cond(IndexState.dark_mode, "main-grid dark-mode", "main-grid"),
        ),
        on_mount=[IndexState.add_medicamento, IndexState.recompute],
    )


def get_page():  # export
    return index_page()

__all__ = ["get_page", "index_page", "IndexState"]
