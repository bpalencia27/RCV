from __future__ import annotations
from rcvco.adapters.llm.base import SupportsGenerate
from typing import Dict, Any

KEY_LABS = {
    "CREATININA EN SUERO U OTROS": "creat",
    "HEMOGLOBINA GLICOSILADA (HBA1C)": "hba1c",
    "COLESTEROL LDL": "ldl",
}

def build_prompt(data: Dict[str, Any]) -> str:
    labs = data.get("labs", [])
    meds = data.get("medications", [])
    idx = {l.get("nombre"): l for l in labs}
    partes: list[str] = []
    for canonical, short in KEY_LABS.items():
        if canonical in idx:
            v = idx[canonical].get("valor")
            partes.append(f"{short}={v}")
    factores = []
    if data.get("has_dm"): factores.append("DM")
    if data.get("has_hta"): factores.append("HTA")
    if data.get("peso_kg"): factores.append(f"peso={data['peso_kg']}")
    resumen = ", ".join(partes) or "sin labs clave"
    fx = ",".join(factores) or "sin factores"
    return (
        f"Paciente {data.get('pseudo_id')} edad {data.get('edad')} sexo {data.get('sexo')} "
        f"({fx}); labs: {resumen}; medicamentos={len(meds)}. Genera informe clínico breve con prioridades y recomendaciones resumidas."
    )

def build_and_generate_report(client: SupportsGenerate, data: Dict[str, Any]) -> str:
    prompt = build_prompt(data)
    return client.generate_report(prompt)
