---
applyTo: "**"
description: "Refactor seguro sin alterar semántica clínica"
---

# RCV-CO • Refactor Coach

- No cambies reglas clínicas ni semántica de negocio.  
- Modulariza: `labs`, `risk`, `scoring`, `tfg`, `report`, `ingest` (parseo PDF/TXT).  
- Extrae funciones puras: `agenda_labs`, `clasificar_riesgo_cv_4_pasos`, `calcula_puntaje`, `crcl_cockcroft_gault`, `generar_informe`.  
- UI (Reflex): sin lógica clínica; delega a servicios.  
- Cada refactor viene con **tests** + **black/ruff**; salida: resumen, diff, notas, TODOs (≤5), lista de tests.
- Mantén documentación actualizada: `README.md`, `docs/`, comentarios en código.