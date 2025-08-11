import reflex as rx
from .layout import section, container

# Tarjetas de características que se pueden insertar dentro del panel inferior o antes del informe.

_DEF_ICON = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round' class='w-8 h-8'><path d='M12 3l9 4-9 4-9-4 9-4z'/><path d='M3 17l9 4 9-4'/><path d='M3 12l9 4 9-4'/></svg>"""

def feature_card(title: str, text: str, icon_svg: str | None = None):
    icon = icon_svg or _DEF_ICON
    return rx.box(
        rx.hstack(
            rx.html(icon, class_name="text-[var(--primary)]"),
            rx.heading(title, class_name="text-base font-semibold"),
            spacing="3",
            align_items="center",
        ),
        rx.text(text, class_name="content text-sm mt-2"),
        class_name="card h-full",
    )

def features_grid(items: list[dict]):
    return section(
        container(
            rx.grid(
                *[feature_card(i["title"], i["text"], i.get("icon")) for i in items],
                class_name="grid gap-5 md:grid-cols-3"
            )
        )
    )
