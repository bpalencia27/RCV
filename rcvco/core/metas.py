"""Cálculo de metas y puntuaciones por programa."""

from typing import Dict, Optional, Union
import logging

def calcular_puntuacion_metas(
    programa: str,
    tfg: float,
    glicemia: float,
    ldl_actual: float,
    ldl_previo: Optional[float],
    hdl: float,
    trigliceridos: float,
    pa_sistolica: int,
    pa_diastolica: int,
    rac: float,
    peso_actual: float,
    peso_previo: Optional[float],
    perimetro: float,
    sexo: str,
    edad: int,
    riesgo_cv: Optional[str] = None,
    hba1c: Optional[float] = None,
    tiene_ecv: bool = False,
    tiene_dm: bool = False
) -> Dict[str, Union[float, int]]:
    """Calcula puntuación según metas del programa.
    
    Args:
        programa: 'HTA', 'DM' o 'ERC'
        tfg: TFG en mL/min
        glicemia: mg/dL
        ldl_actual: mg/dL
        ldl_previo: mg/dL o None
        hdl: mg/dL
        trigliceridos: mg/dL
        pa_sistolica: mmHg
        pa_diastolica: mmHg
        rac: mg/g
        peso_actual: kg
        peso_previo: kg o None
        perimetro: cm
        sexo: 'm' o 'f'
        edad: años
        riesgo_cv: Nivel de riesgo CV
        hba1c: % o None
        tiene_ecv: Presencia de ECV
        tiene_dm: Diagnóstico de DM
        
    Returns:
        Dict con puntajes por meta y total
    
    Raises:
        ValueError: Si el programa es inválido
    """
    if programa not in ["HTA", "DM", "ERC"]:
        raise ValueError("Programa debe ser 'HTA', 'DM' o 'ERC'")
        
    puntos = {
        "total": 0,
        "glicemia": 0,
        "ldl": 0,
        "hdl": 0,
        "trigliceridos": 0,
        "pa": 0,
        "rac": 0,
        "imc": 0,
        "perimetro": 0,
        "hba1c": 0
    }
    
    # Ajusta pesos según programa y estadio ERC
    if programa == "HTA":
        # Glicemia (5)
        if 60 <= glicemia <= 100:
            puntos["glicemia"] = 5
            
        # LDL (25)
        if riesgo_cv in ["ALTO", "MUY ALTO"] or (ldl_previo and ldl_previo >= 190 and ldl_actual <= ldl_previo * 0.5):
            if ldl_actual <= 100:
                puntos["ldl"] = 25
        elif riesgo_cv not in ["ALTO", "MUY ALTO"] and ldl_actual <= 130:
            puntos["ldl"] = 25
            
        # HDL (5)
        if (sexo == "m" and hdl >= 40) or (sexo == "f" and hdl >= 50):
            puntos["hdl"] = 5
            
        # Triglicéridos (5)
        if trigliceridos <= 150:
            puntos["trigliceridos"] = 5
            
        # PA (25)
        if edad < 60 and pa_sistolica <= 140 and pa_diastolica <= 90:
            puntos["pa"] = 25
        elif edad >= 60 and pa_sistolica <= 150 and pa_diastolica <= 90:
            puntos["pa"] = 25
            
        # RAC (25)
        if rac <= 30:
            puntos["rac"] = 25
            
        # IMC (5)
        if peso_previo and peso_actual <= peso_previo * 0.95:
            puntos["imc"] = 5
            
        # Perímetro (5)
        if (sexo == "m" and perimetro <= 94) or (sexo == "f" and perimetro <= 90):
            puntos["perimetro"] = 5
            
    elif programa == "DM":
        # Glicemia (4)
        if 70 <= glicemia <= 130:
            puntos["glicemia"] = 4
            
        # LDL (20)
        if ldl_actual <= 100:
            puntos["ldl"] = 20
        elif 101 <= ldl_actual <= 129 and ldl_previo and ldl_actual <= ldl_previo * 0.9:
            puntos["ldl"] = 20
        elif 130 <= ldl_actual <= 189 and ldl_previo and ldl_actual <= ldl_previo * 0.7:
            puntos["ldl"] = 20
        elif ldl_actual >= 190 and ldl_previo and ldl_actual <= ldl_previo * 0.5:
            puntos["ldl"] = 20
            
        # HDL (4)
        if (sexo == "m" and hdl >= 40) or (sexo == "f" and hdl >= 50):
            puntos["hdl"] = 4
            
        # Triglicéridos (4)
        if trigliceridos <= 150:
            puntos["trigliceridos"] = 4
            
        # PA (20)
        if pa_sistolica <= 140 and pa_diastolica <= 90:
            puntos["pa"] = 20
            
        # RAC (20)
        if rac <= 30:
            puntos["rac"] = 20
            
        # IMC (4)
        if peso_previo and peso_actual <= peso_previo * 0.95:
            puntos["imc"] = 4
            
        # Perímetro (4)
        if (sexo == "m" and perimetro <= 94) or (sexo == "f" and perimetro <= 90):
            puntos["perimetro"] = 4
            
        # HbA1c (20)
        if hba1c is not None:
            if edad <= 65 and not tiene_ecv and hba1c <= 7:
                puntos["hba1c"] = 20
            elif (edad > 65 or tiene_ecv) and hba1c <= 8:
                puntos["hba1c"] = 20
                
    else:  # ERC
        es_e4 = tfg <= 30
        
        if es_e4 and tiene_dm:
            # E4 con DM
            if 70 <= glicemia <= 130:
                puntos["glicemia"] = 5
            puntos["ldl"] = 0  # Sin puntos para LDL en E4
            if (sexo == "m" and hdl >= 40) or (sexo == "f" and hdl >= 50):
                puntos["hdl"] = 5
            if trigliceridos <= 150:
                puntos["trigliceridos"] = 5
            if pa_sistolica <= 140 and pa_diastolica <= 90:
                puntos["pa"] = 30
            if rac <= 30:
                puntos["rac"] = 15
            if peso_previo and peso_actual <= peso_previo * 0.95:
                puntos["imc"] = 5
            if (sexo == "m" and perimetro <= 94) or (sexo == "f" and perimetro <= 90):
                puntos["perimetro"] = 5
            if hba1c is not None:
                if edad <= 65 and not tiene_ecv and hba1c <= 7:
                    puntos["hba1c"] = 30
                elif (edad > 65 or tiene_ecv) and hba1c <= 8:
                    puntos["hba1c"] = 30
                    
        elif es_e4:
            # E4 sin DM
            if 70 <= glicemia <= 130:
                puntos["glicemia"] = 10
            puntos["ldl"] = 0  # Sin puntos para LDL en E4
            if (sexo == "m" and hdl >= 40) or (sexo == "f" and hdl >= 50):
                puntos["hdl"] = 10
            if trigliceridos <= 150:
                puntos["trigliceridos"] = 10
            if pa_sistolica <= 140 and pa_diastolica <= 90:
                puntos["pa"] = 40
            if rac <= 30:
                puntos["rac"] = 10
            if peso_previo and peso_actual <= peso_previo * 0.95:
                puntos["imc"] = 10
            if (sexo == "m" and perimetro <= 94) or (sexo == "f" and perimetro <= 90):
                puntos["perimetro"] = 10
                
        elif tiene_dm:
            # E1-E3 con DM
            if 70 <= glicemia <= 130:
                puntos["glicemia"] = 4
            if ldl_actual <= 100:
                puntos["ldl"] = 20
            if (sexo == "m" and hdl >= 40) or (sexo == "f" and hdl >= 50):
                puntos["hdl"] = 4
            if trigliceridos <= 150:
                puntos["trigliceridos"] = 4
            if pa_sistolica <= 140 and pa_diastolica <= 90:
                puntos["pa"] = 20
            if rac <= 30:
                puntos["rac"] = 20
            if peso_previo and peso_actual <= peso_previo * 0.95:
                puntos["imc"] = 4
            if (sexo == "m" and perimetro <= 94) or (sexo == "f" and perimetro <= 90):
                puntos["perimetro"] = 4
            if hba1c is not None:
                if edad <= 65 and not tiene_ecv and hba1c <= 7:
                    puntos["hba1c"] = 20
                elif (edad > 65 or tiene_ecv) and hba1c <= 8:
                    puntos["hba1c"] = 20
                    
        else:
            # E1-E3 sin DM
            if 70 <= glicemia <= 130:
                puntos["glicemia"] = 5
            if ldl_actual <= 100:
                puntos["ldl"] = 25
            if (sexo == "m" and hdl >= 40) or (sexo == "f" and hdl >= 50):
                puntos["hdl"] = 5
            if trigliceridos <= 150:
                puntos["trigliceridos"] = 5
            if pa_sistolica <= 140 and pa_diastolica <= 90:
                puntos["pa"] = 25
            if rac <= 30:
                puntos["rac"] = 25
            if peso_previo and peso_actual <= peso_previo * 0.95:
                puntos["imc"] = 5
            if (sexo == "m" and perimetro <= 94) or (sexo == "f" and perimetro <= 90):
                puntos["perimetro"] = 5
                
    puntos["total"] = sum(puntos.values())
    return puntos
