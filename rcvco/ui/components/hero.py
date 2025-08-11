import reflex as rx
from .layout import container, section

# Hero reutilizable basado en la estructura actual (sin romper el grid principal)

def hero(title: str, subtitle: str, cta_label: str = "Empezar", on_click=None):
    return section(
        container(
            rx.vstack(
                rx.heading(title, class_name="text-4xl font-extrabold tracking-tight"),
                rx.text(subtitle, class_name="text-base md:text-lg content max-w-2xl"),
                rx.hstack(
                    rx.button(
                        cta_label,
                        on_click=on_click,
                        class_name="bg-[var(--primary)] hover:bg-[var(--primary-accent)] text-white font-semibold px-6 py-3 rounded-lg shadow"),
                    spacing="4",
                    class_name="pt-4 flex-wrap",
                ),
                spacing="5",
                align_items="start",
            )
        ),
        alt=True,
    )
