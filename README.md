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

## Próximos pasos
Ver TODOs en planificación.
