---
mode: "agent"
description: "Refactor seguro (sin cambiar clínica) + tests y linters"
---

# RCV-CO • Refactor Integral

**Pasos**
1) Mapa de olores (duplicación, funciones largas, mezcla UI/negocio, falta de typing/tests).  
2) Plan por impacto/riesgo.  
3) Aplicación: extrae funciones puras en `rcvco/domain`, separa UI/servicios, añade typing/docstrings, manejo de errores, logs.  
4) **Tests**: rangos X–Y, unificación, PA edad, LDL×RCV, HbA1c, 4 Pasos, CrCl.  
5) Verificación: **black**, **ruff**, **pytest**.

**Salida**
- Resumen • Patch (diff) • Notas técnicas • TODOs (≤5) • Lista de tests.  
**Encabezado**: “✓ Refactor RCV-CO v2.0 | Sin cambios funcionales: <sí/no> | Cobertura core ≥80%: <sí/no>”.
- **Documentación**: actualiza `README.md`, `docs/`, comentarios en código.