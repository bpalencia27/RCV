---
applyTo: "**"
description: "Stack obligado y prácticas de código para RCV-CO"
---

# RCV-CO • Stack (Python + Reflex) y prácticas

- Lenguaje: **Python**. UI: **Reflex** para todas las páginas.  
- Formateo: **black**. Linter: **ruff**. Tipado: PEP 484.  
- Validación: **pydantic** en DTO/inputs. Logs estructurados.  
- Seguridad: no exponer PII/PHI; manejo de errores en capa borde (endpoints/acciones UI).  
- Tests: **pytest** + **httpx** (API); pruebas funcionales UI cuando aplique; cobertura **≥80%** en core.  
- Fechas: ISO8601, TZ **America/Bogota**.  
- Refactor continuo (DRY/KISS/SOLID). Separar dominio/infra/UI.
