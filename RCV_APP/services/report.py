"""
Generación de informes clínicos.

Este módulo implementa la generación de informes para
evaluación de riesgo cardiovascular y seguimiento.
"""

from __future__ import annotations
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from RCV_APP.services.labs import AgendaItem


@dataclass
class Informe:
    """Informe clínico."""
    generado_en: datetime
    texto: str
    titulo: str
    formato: str = "html"
    
    @property
    def fecha_generacion_str(self) -> str:
        """Retorna la fecha de generación en formato legible."""
        return self.generado_en.strftime("%d/%m/%Y %H:%M")


def generar_informe_simple(
    nombre_paciente: str,
    edad: int,
    sexo: str,
    riesgo_categoria: str,
    puntaje: int,
    ascvd: Optional[float] = None,
    aclaramiento_creatinina: Optional[float] = None,
    agenda: Optional[List[AgendaItem]] = None
) -> Informe:
    """
    Genera un informe simple en texto plano.
    
    Args:
        nombre_paciente: Nombre del paciente
        edad: Edad del paciente
        sexo: Sexo del paciente (M/F)
        riesgo_categoria: Categoría de riesgo
        puntaje: Puntaje numérico
        ascvd: Riesgo ASCVD a 10 años (%)
        aclaramiento_creatinina: TFG (ml/min)
        agenda: Lista de items de agenda
        
    Returns:
        Informe con texto plano
    """
    lineas: list[str] = []
    lineas.append("EVALUACIÓN DE RIESGO CARDIOVASCULAR Y SEGUIMIENTO")
    lineas.append("=" * 50)
    lineas.append(f"Paciente: {nombre_paciente}")
    lineas.append(f"Edad: {edad} años")
    lineas.append(f"Sexo: {'Masculino' if sexo == 'M' else 'Femenino'}")
    lineas.append("-" * 50)
    lineas.append(f"Categoría de riesgo: {riesgo_categoria} (puntaje {puntaje}).")
    
    if ascvd is not None:
        lineas.append(f"Riesgo estimado a 10 años: {ascvd:.1f}%.")
        
    if aclaramiento_creatinina is not None:
        lineas.append(
            f"Aclaramiento de creatinina estimado: {aclaramiento_creatinina} ml/min."
        )
        
    if agenda:
        lineas.append("-" * 50)
        lineas.append("Próximos laboratorios programados:")
        for a in agenda:
            lineas.append(
                f" - {a.examen}: {a.fecha_programada.strftime('%d/%m/%Y')} "
                f"(Revisión: {a.revision_fecha.strftime('%d/%m/%Y')})"
            )
            
    texto = "\n".join(lineas)
    return Informe(
        generado_en=datetime.now(),
        texto=texto,
        titulo=f"Informe RCV - {nombre_paciente}"
    )


def generar_informe_html(
    nombre_paciente: str,
    edad: int,
    sexo: str,
    riesgo_categoria: str,
    puntaje: int,
    ascvd: Optional[float] = None,
    aclaramiento_creatinina: Optional[float] = None,
    estadio_erc: Optional[str] = None,
    agenda: Optional[List[AgendaItem]] = None
) -> Informe:
    """
    Genera un informe completo en formato HTML.
    
    Args:
        nombre_paciente: Nombre del paciente
        edad: Edad del paciente
        sexo: Sexo del paciente (M/F)
        riesgo_categoria: Categoría de riesgo
        puntaje: Puntaje numérico
        ascvd: Riesgo ASCVD a 10 años (%)
        aclaramiento_creatinina: TFG (ml/min)
        estadio_erc: Estadio ERC
        agenda: Lista de items de agenda
        
    Returns:
        Informe con texto HTML
    """
    # Mapa de colores para categorías de riesgo
    color_mapa = {
        "Muy Alto": "darkred",
        "Alto": "red",
        "Moderado": "orange",
        "Bajo": "green"
    }
    
    color_riesgo = color_mapa.get(riesgo_categoria, "gray")
    
    # Construir el HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Informe RCV - {nombre_paciente}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                border: 1px solid #ddd;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #eee;
            }}
            .section {{
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 1px solid #eee;
            }}
            .risk-category {{
                display: inline-block;
                padding: 5px 10px;
                background-color: {color_riesgo};
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 10px 0;
            }}
            table, th, td {{
                border: 1px solid #ddd;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f4f4f4;
            }}
            .footer {{
                font-size: 0.8em;
                text-align: center;
                margin-top: 20px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Evaluación de Riesgo Cardiovascular</h1>
                <p>Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
            </div>
            
            <div class="section">
                <h2>Información del Paciente</h2>
                <p><strong>Nombre:</strong> {nombre_paciente}</p>
                <p><strong>Edad:</strong> {edad} años</p>
                <p><strong>Sexo:</strong> {'Masculino' if sexo == 'M' else 'Femenino'}</p>
            </div>
            
            <div class="section">
                <h2>Evaluación de Riesgo</h2>
                <p><strong>Categoría de Riesgo:</strong> <span class="risk-category">{riesgo_categoria}</span></p>
                <p><strong>Puntaje:</strong> {puntaje}</p>
                {f'<p><strong>Riesgo ASCVD a 10 años:</strong> {ascvd:.1f}%</p>' if ascvd is not None else ''}
                {f'<p><strong>Aclaramiento de Creatinina:</strong> {aclaramiento_creatinina} ml/min</p>' if aclaramiento_creatinina is not None else ''}
                {f'<p><strong>Estadio ERC:</strong> {estadio_erc}</p>' if estadio_erc is not None else ''}
            </div>
    """
    
    # Agregar sección de agenda si existe
    if agenda:
        html += f"""
            <div class="section">
                <h2>Próximos Laboratorios</h2>
                <table>
                    <tr>
                        <th>Examen</th>
                        <th>Fecha Programada</th>
                        <th>Motivo</th>
                        <th>Fecha de Revisión</th>
                    </tr>
        """
        
        for item in agenda:
            html += f"""
                    <tr>
                        <td>{item.examen}</td>
                        <td>{item.fecha_programada.strftime('%d/%m/%Y')}</td>
                        <td>{item.motivo}</td>
                        <td>{item.revision_fecha.strftime('%d/%m/%Y')}</td>
                    </tr>
            """
            
        html += """
                </table>
            </div>
        """
    
    # Agregar recomendaciones generales según categoría de riesgo
    recomendaciones = {
        "Muy Alto": """
            <li>Control estricto de factores de riesgo cardiovascular</li>
            <li>Seguimiento médico frecuente (cada 1-3 meses)</li>
            <li>Cumplimiento estricto de medicación</li>
            <li>Dieta baja en sal y grasas saturadas</li>
            <li>Actividad física supervisada</li>
        """,
        "Alto": """
            <li>Control regular de factores de riesgo cardiovascular</li>
            <li>Seguimiento médico cada 3-6 meses</li>
            <li>Cumplimiento de medicación</li>
            <li>Dieta saludable</li>
            <li>Actividad física regular</li>
        """,
        "Moderado": """
            <li>Control de factores de riesgo cardiovascular</li>
            <li>Seguimiento médico cada 6-12 meses</li>
            <li>Estilo de vida saludable</li>
            <li>Actividad física regular</li>
        """,
        "Bajo": """
            <li>Mantenimiento de estilo de vida saludable</li>
            <li>Seguimiento médico anual</li>
            <li>Actividad física regular</li>
        """
    }
    
    html += f"""
            <div class="section">
                <h2>Recomendaciones Generales</h2>
                <ul>
                    {recomendaciones.get(riesgo_categoria, '')}
                </ul>
            </div>
            
            <div class="footer">
                <p>Este informe fue generado por el sistema CardiaIA - RCV-CO.</p>
                <p>La información contenida es orientativa y no sustituye el criterio médico.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return Informe(
        generado_en=datetime.now(),
        texto=html,
        titulo=f"Informe RCV - {nombre_paciente}",
        formato="html"
    )


__all__ = [
    "generar_informe_simple",
    "generar_informe_html",
    "Informe"
]
