from __future__ import annotations
from rcvco.adapters.llm.base import SupportsGenerate
from typing import Dict, Any

def build_prompt(data: Dict[str, Any]) -> str:
    return f"Genera informe clínico breve para paciente {data.get('pseudo_id')} con {len(data.get('labs', []))} laboratorios."

def build_and_generate_report(client: SupportsGenerate, data: Dict[str, Any]) -> str:
    prompt = build_prompt(data)
    return client.generate_report(prompt)
