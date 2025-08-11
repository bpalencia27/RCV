# PLAN.md — Implementación Iterativa RCV-CO (Reflex + Backend dominio existente)

Fecha: 2025-08-11
Python: 3.11.9
Reflex: 0.8.3 (ya presente)

## Objetivo Global
UI en Reflex que permita flujo clínico completo (captura datos, parsing labs PDF/TXT, cálculo riesgo CV consenso dislipidemia 2024 con reglas ya disponibles en dominio, clasificación ERC vía Cockcroft–Gault, evaluación fragilidad (Fried), validación de medicamentos (+ sugerencias IA), plan de seguimiento y generación de informe) reutilizando lógica de dominio existente (`rcvco.domain.*`).

## Principios
- Reusar primero (`rcvco.domain.*`) – no duplicar fórmulas / constantes.
- Extensiones mínimas: sólo añadir archivos para brechas (parser, AI dosing provider, catálogos UI, generación informe UI).
- PRs pequeños; cada PR incluye: resumen, checklist, pruebas (unit y/o e2e), lint OK.
- Código tipado, docstrings, black + ruff.
- Persistencia: usar modelos / patrón repos existente (si falta repo de medicamentos, crear mínimo).

## Brechas Detectadas (pre-auditoría profunda)
1. Archivos JS legacy (`assets/legacy`) deberán ser reemplazados por componentes Reflex / estado central.  
2. Placeholders e incompletos en dominio (`assistant.py`, `calculos.py`, etc.) – completar lógica pendiente respetando reglas existentes.  
3. Falta capa de parsing PDF/TXT (crear en `rcvco/services/parsing/`).  
4. Falta interfaz desacoplada para proveedor IA (dosing / resumen).  
5. Falta generación de informe consolidado desde UI Reflex (render + descarga).  
6. Falta catálogos unificados (factores de riesgo, potenciadores, lista validable de labs).  
7. Falta validación estructurada de medicamentos (dosis segura según TFG, fragilidad).  
8. Empaquetado Render (Dockerfile, render.yaml / Procfile).  
9. E2E con Playwright para interacciones clave (fragilidad, carga labs, modales).  
10. Tests para parser y cálculos (Cockcroft–Gault, riesgo CV, validación medicamentos).  

## Árbol de Archivos Propuesto (nuevos / modificados)
```
rcvco/
  ui/
    state/
      form_state.py          # Estado principal Reflex (paciente + labs + meds + riesgo)
    components/
      forms.py               # Secciones del formulario
      labs.py                # Tabla/edición laboratorios
      meds.py                # Gestión medicamentos
      fragilidad.py          # Escala Fried + resultado
      risk_panel.py          # Panel riesgo + metas
      report_view.py         # Vista previa informe
      modals.py              # Componentes de modales reutilizables
    catalogs.py              # Catálogos (factores, potenciadores, mapeo labs) [derive dominio cuando posible]
    report_builder.py        # Orquestar construcción del informe (usa dominio + servicios)
    dosing_validator.py      # Lógica de validación dosis (usa TFG, fragilidad)
  services/
    parsing/
      __init__.py
      pdf_parser.py          # Extracción texto estructurado
      txt_parser.py          # Parsing líneas claves
      lab_normalizer.py      # Map a nombres estándar dominio
    ai/
      __init__.py
      provider_base.py       # AiDosingProvider (interfaz)
      gemini_provider.py     # Implementación si clave disponible
      openai_provider.py     # (opcional fallback)
  repositories/
    medicamentos_repo.py     # Persistencia medicamentos (SQLModel)
  api/
    endpoints_meds.py        # CRUD mínimo medicamentos
    endpoints_parse.py       # Endpoint subir archivo -> JSON labs normalizados

Dockerfile
render.yaml
Procfile (si necesario para workers)
PLAN.md (este)
```

## Dependencias (pin exacto — revisar compatibilidad durante implementación)
(Refleja libs ya instaladas + nuevas; ajustar sólo si conflicto)
```
fastapi==0.116.1
starlette==0.47.2
pydantic==2.11.7
sqlalchemy==2.0.43
sqlmodel==0.0.24
alembic==1.16.4
uvicorn==0.35.0
python-multipart==0.0.20
redis==6.4.0         # si se usa cache IA / colas (opcional, confirmar)
httpx==0.28.1
jinja2==3.1.6        # si se usa para plantilla informe (opcional)
reflex==0.8.3
PyPDF2==3.0.1        # parsing PDF básico (sin OCR)
pdfminer.six==20240706 # extracción granular alternativa
python-dotenv==1.1.1
rich==14.1.0
psutil==7.0.0
watchfiles==1.1.0
websockets==15.0.1
# IA proveedores (instalar condicional)
openai==1.40.0       # si se configura
google-generativeai==0.8.3  # si se configura Gemini
```
(Nota: OCR no incluido inicialmente; añadir `pytesseract` sólo si se detecta necesidad de imágenes escaneadas.)

## Métricas / Criterios de Listo
- Riesgo CV y TFG recalculan <200ms en interacción.
- Parser labs: ≥90% campos soportados si presentes en texto estándar.
- Cobertura tests módulos core (parsing, riesgo, TFG, meds) ≥80%.
- Informe descargable (PDF o HTML imprimible) con secciones completas.
- Sin duplicados de medicamentos; validaciones disparan alerta consistente.
- Modales accesibles (foco gestionado, Escape cierra, backdrop).  

## Roadmap de PRs Pequeños
1. PR1 Base Infra & Catálogos: crear `catalogs.py`, esqueleto `form_state.py`, configurar ruff/black, Dockerfile inicial, render.yaml.  
   Aceptación: app arranca, estado base sin lógica avanzada.  
2. PR2 Completar placeholders dominio pendientes (rellenar lógica faltante en `assistant.py`, `calculos.py`, etc. sin romper tests existentes).  
   Aceptación: tests Cockcroft-Gault existentes pasan.  
3. PR3 Componentes UI Form (datos básicos + labs manuales + Fried UI sin lógica).  
   Aceptación: se renderizan componentes y capturan inputs.  
4. PR4 Lógica Cálculo en Estado (TFG, riesgo CV usando dominio, fragilidad y auto-marcado programa).  
   Aceptación: cambios de inputs actualizan panel riesgo.  
5. PR5 Parsing TXT/PDF + normalización labs + tests parser.  
   Aceptación: subir archivo llena campos; tests >80% paths.  
6. PR6 Gestión Medicamentos (modelo, repo, endpoints, UI lista, validación dosis básica).  
   Aceptación: crear/listar sin duplicar; validación TFG/fragilidad.  
7. PR7 AI Dosing Provider (interfaz + stub + configuración), sugerencias en UI.  
   Aceptación: stub retorna recomendación simulada; interfaz intercambiable.  
8. PR8 Generación Informe (builder + vista + descarga).  
   Aceptación: informe contiene todas secciones y fechas seguimiento (+7 días).  
9. PR9 Empaquetado Render (refinar Dockerfile, Procfile, healthcheck) + documentación despliegue.  
   Aceptación: despliegue exitoso manual.  
10. PR10 E2E Playwright (checklist interacciones clave).  
   Aceptación: suite verde en CI.  
11. PR11 Optimización / Accesibilidad / Limpieza Legacy (eliminar assets legacy no usados).  
   Aceptación: no se rompe funcionalidad; lighthouse accesibilidad >90%.  

## Riesgos y Mitigación
- Parsing variable: aislar reglas por regex + tabla mapping -> fácil extender.
- Proveedor IA inestable: fallback stub garantizado.
- Divergencia de reglas clínicas: sólo consumir dominio; no hardcode en UI.
- Performance: diferir cálculos costosos (memoización simple en estado).  

## Próximo Paso (PR1)
1. Auditar dominio actual para extraer catálogos (labs names, factores).  
2. Crear `rcvco/ui/catalogs.py` (placeholders + TODO derivar de dominio) y `rcvco/ui/state/form_state.py` esqueleto.  
3. Añadir Dockerfile y render.yaml básicos.  
4. Config ruff/black si no presentes.  

(Se ejecutará en la siguiente iteración / Step 2.)
