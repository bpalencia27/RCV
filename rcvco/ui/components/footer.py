import reflex as rx
from .layout import section, container

# Footer manteniendo estética neutral; adaptable a tema actual

def footer(columns: list[dict]):
    return section(
        container(
            rx.grid(
                *[
                    rx.box(
                        rx.heading(col["title"], class_name="text-sm font-bold uppercase tracking-wide mb-3"),
                        rx.vstack(
                            *[rx.link(l["label"], href=l.get("href", "#"), class_name="text-sm content hover:underline") for l in col.get("links", [])],
                            spacing="1"
                        ),
                        class_name="min-w-[140px]"
                    ) for col in columns
                ],
                class_name="grid gap-8 sm:grid-cols-2 md:grid-cols-4"
            ),
            rx.box(
                rx.text("© 2025 Plataforma Clínica", class_name="text-xs content mt-8"),
                class_name="border-t border-[var(--border-color)] pt-4 mt-4"
            )
        ),
        alt=True
    )
