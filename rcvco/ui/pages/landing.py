import reflex as rx
from rcvco.ui.theme import theme
from rcvco.ui.components.hero import hero
from rcvco.ui.components.cards import features_grid
from rcvco.ui.components.accordion import accordion
from rcvco.ui.components.footer import footer
from rcvco.ui.components.seo import seo_head

# Página landing que reutiliza el framework actual sin alterar index principal.

def landing_page():
    feats = [
        {"title": "Evaluación ERC", "text": "Ingreso de parámetros clínicos y cálculo TFG dinámico."},
        {"title": "Riesgo CV", "text": "Clasificación estratificada con factores modificables."},
        {"title": "Informe Asistido", "text": "Generación de resumen clínico para decisiones rápidas."},
    ]
    faq = [
        ("¿Cómo calculan IMC / TFG?", "Se aplican fórmulas simples; puede ajustarse en futuras versiones."),
        ("¿Se guarda información?", "Historial local temporal; integrar backend es opcional."),
    ]
    cols = [
        {"title": "Producto", "links": [{"label": "Panel"}, {"label": "Metas"}]},
        {"title": "Recursos", "links": [{"label": "FAQ"}, {"label": "Guía"}]},
        {"title": "Legal", "links": [{"label": "Privacidad"}, {"label": "Términos"}]},
        {"title": "Soporte", "links": [{"label": "Contacto"}]},
    ]
    return rx.box(
        theme(),
        seo_head("Plataforma Clínica", "Gestión integral de parámetros ERC y riesgo CV."),
        hero("Plataforma Clínica Integral", "Monitoriza variables renales y riesgo cardiovascular en un entorno unificado.", "Ir al Panel", on_click=lambda: rx.redirect("/")),
        features_grid(feats),
        accordion(faq),
        footer(cols),
        class_name="landing-root",
    )


def get_page():
    return landing_page()

__all__ = ["get_page", "landing_page"]
