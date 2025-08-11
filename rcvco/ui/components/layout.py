import reflex as rx

# Contenedor y secciones reutilizando el framework actual (grid principal y paneles)

def container(*children, size: str = "lg", **props):
    maxw = {"sm": "640px", "md": "820px", "lg": "1100px", "xl": "1280px"}.get(size, "1100px")
    return rx.box(
        *children,
        style={"maxWidth": maxw, "margin": "0 auto", "padding": "0 1.5rem", "width": "100%"},
        **props,
    )

def section(*children, padded: bool = True, alt: bool = False, **props):
    bg = "var(--bg-panel-alt)" if alt else "transparent"
    return rx.box(
        *children,
        style={
            "padding": "3.25rem 0" if padded else "1rem 0",
            "background": bg,
        },
        **props,
    )
