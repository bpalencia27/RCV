# RCV-CO

Scaffold inicial para aplicación Reflex de evaluación de riesgo cardiovascular.

## Ejecutar

```powershell
pip install .[dev]
reflex run
pytest
```

## Estructura
- domain: lógica clínica (labs, scoring, riesgo, TFG, reportes)
- ingest: parsers de archivos (txt/pdf placeholder)
- ui: página Reflex `paciente`
- tests: casos básicos
 
 ## Desarrollo
 
 ### Variables entorno
 Copiar `.env.example` a `.env` y ajustar llaves.
 
 ### Comandos Make
 `make install` instalar dependencias.
 `make run` inicia API FastAPI (uvicorn).
 `make test` ejecuta tests.
 `make lint` ruff + mypy.
 `make format` black + autofix.
 
 ### Flujo
 1. Subir PDF/labs -> /api/upload
 2. Rellenar formulario -> /api/report
 3. Mostrar reporte.
 
 Ver `docs/ARCHITECTURE.md` para capas.

### Pruebas E2E (Playwright)
Se añadió configuración inicial (`package.json`, `playwright.config.ts`, carpeta `e2e/`).
Pasos básicos:
1. Node 18+ instalado.
2. `npm install`
3. `npx playwright install`
4. Correr headless: `npm run e2e` / UI: `npm run e2e:ui`
5. Ajustar selectores placeholder en specs (`upload_autofill`, `medication_dedupe`).
6. Reporte: `npm run e2e:report` (genera html).

## Próximos pasos
Ver TODOs en planificación.
