"""Clasificación de riesgo cardiovascular usando el protocolo de 4 pasos."""

from typing import Dict, Union
import logging

def clasificar_riesgo_cv_4_pasos(
    tfg: float,
    tiene_ecv: bool,
    tiene_dm: bool,
    tiene_hta: bool,
    dano_organo: bool,
    duracion_dm_10_anos: bool,
    pa_sistolica: int,
    pa_diastolica: int,
    ldl: float,
    factores_riesgo: int,
    rac: float
) -> Dict[str, str]:
    """Evalúa el riesgo cardiovascular usando el protocolo de 4 pasos.
    
    Args:
        tfg: TFG en mL/min
        tiene_ecv: Presencia de ECV aterosclerótica establecida
        tiene_dm: Diagnóstico de diabetes
        tiene_hta: Diagnóstico de hipertensión
        dano_organo: Presencia de daño en órgano blanco
        duracion_dm_10_anos: DM con duración >10 años
        pa_sistolica: PA sistólica en mmHg
        pa_diastolica: PA diastólica en mmHg
        ldl: Colesterol LDL en mg/dL
        factores_riesgo: Número de factores de riesgo adicionales
        rac: Relación albúmina/creatinina en mg/g
        
    Returns:
        Dict con nivel de riesgo y justificación
    """
    justificacion = []
    
    # PASO 1: MUY ALTO RIESGO
    if tiene_ecv:
        justificacion.append("ECV establecida")
    if tfg <= 30:
        justificacion.append("TFG ≤ 30")
    if tiene_dm and (dano_organo or factores_riesgo >= 3 or duracion_dm_10_anos):
        if dano_organo:
            justificacion.append("Diabetes con daño de órgano")
        elif factores_riesgo >= 3:
            justificacion.append("Diabetes con ≥3 factores de riesgo")
        else:
            justificacion.append("Diabetes >10 años de duración")
            
    if justificacion:  # Si hay cualquier criterio de Muy Alto
        return {
            "nivel": "MUY ALTO",
            "justificacion": "; ".join(justificacion)
        }
    
    # PASO 2: ALTO RIESGO
    justificacion = []
    if 30 < tfg <= 60:
        justificacion.append("TFG entre 30-60")
    if pa_sistolica >= 180 or pa_diastolica >= 110:
        justificacion.append("PA ≥ 180/110")
    if ldl > 190:
        justificacion.append("LDL >190")
    if factores_riesgo >= 3:
        justificacion.append("≥3 factores de riesgo")
        
    if justificacion:  # Si hay cualquier criterio de Alto
        return {
            "nivel": "ALTO",
            "justificacion": "; ".join(justificacion)
        }
    
    # PASO 3: MODERADO/ALTO POR POTENCIADORES
    if rac > 30:  # RAC como potenciador
        factores_riesgo += 1
        
    if 1 <= factores_riesgo <= 2:
        return {
            "nivel": "MODERADO",
            "justificacion": f"{factores_riesgo} factores de riesgo presentes"
        }
    elif factores_riesgo >= 3:
        return {
            "nivel": "ALTO",
            "justificacion": "≥3 factores de riesgo potenciadores"
        }
    
    # PASO 4: Sin factores significativos
    return {
        "nivel": "BAJO",
        "justificacion": "Sin factores de riesgo significativos"
    }
