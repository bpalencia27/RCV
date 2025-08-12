---
mode: "agent"
description: "Scaffold end-to-end de la web RCV-CO (Python + Reflex) con reglas clínicas y tests"
---

# RCV-CO • Scaffold Web (Python + Reflex)

**Objetivo:** crear/actualizar un proyecto **Reflex** + módulos Python que:
- Ingesta datos (PDF/TXT/JSON) → normaliza labs (usar etiqueta exacta “CREATININA EN SUERO U OTROS”; descartar creatinina orina parcial).  
- Calcula **agenda de labs** (regla X–Y + unificación + revisión +7).  
- Aplica **prioridad de programas** y **puntajes**.  
- Clasifica **Riesgo CV (4 Pasos)** y genera **informe médico** con **fechas exactas** y justificación **sin mencionar “pasos”**.  
- Expone UI en Reflex (formularios, tablas, badges, acciones).  
- Incluye **tests** mínimos y configuración de **black/ruff/pytest**.

## Entregables (crear/actualizar)
- `rcvco/domain/models.py` (pydantic DTOs).  
- `rcvco/domain/labs.py` (agenda_labs).  
- `rcvco/domain/scoring.py` (calcula_puntaje).  
- `rcvco/domain/risk.py` (clasificar_riesgo_cv_4_pasos, ascvd ajustado).  
- `rcvco/domain/tfg.py` (crcl_cockcroft_gault).  
- `rcvco/domain/report.py` (generar_informe).  
- `rcvco/ingest/parsers.py` (PDF/TXT → datos, con mapeos de nombres de exámenes).  
- `rcvco/ui/pages/paciente.py` (Reflex: formulario + agenda + score + riesgo + botón “Ajuste TFG”).  
- `rcvco/ui/theme.css` (estilos básicos, accesible).  
- `tests/` con casos límite (rangos X–Y, unificación, PA por edad, LDL por RCV, HbA1c, 4 Pasos, CrCl).  
- `pyproject.toml` o `requirements.txt` (reflex, pydantic, pytest, httpx, black, ruff).  
- Scripts npm opcionales mínimos si se requieren assets (no meter lógica clínica en JS).

## Reglas de diseño
- UI limpia: cards/tablas/badges; mostrar **fechas exactas** y “Revisión: <fecha_labs+7>”.  
- Estado global Reflex (`rx.State`) con `paciente` y `resumen`.  
- Jamás exponer PII; logs sin datos sensibles.  
- Código tipado, testeable, sin lógica clínica en componentes.

## Formato de salida
1) **Plan** (pasos y archivos).  
2) **Código** (bloques por archivo nuevo/modificado).  
3) **Comandos** para instalar y correr.  
4) **Tests** clave (nombres y asserts).  
5) **Siguientes pasos** (TODOs cortos).
