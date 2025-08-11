# Arquitectura RCV

Capas:
- API (FastAPI): rcvco.api.app / routes
- Servicios: lógica orquestación (services/*)
- Adapters LLM: selección proveedor (adapters/llm)
- Parsing: extracción y normalización labs (parsing/*)
- Dominio: modelos clínicos (rcvco.domain.models)

Flujo report:
Upload -> /api/upload -> parser -> frontend rellena -> /api/report -> prompt -> LLM -> texto.

Diagrama (simplificado):

Frontend -> /api/upload -> parser -> (patient,labs)
Frontend -> /api/report -> services.report_service -> adapters.llm -> texto

Medications Set en backend (router) y espejo en frontend state.js
