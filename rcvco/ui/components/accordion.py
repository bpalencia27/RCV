import reflex as rx
from .layout import section, container

# Acordeón simple reutilizable (sin JS externo)

class _AccordionState(rx.State):
    open_indexes: set[int] = set()

    def toggle(self, idx: int):
        s = set(self.open_indexes)
        if idx in s:
            s.remove(idx)
        else:
            s.add(idx)
        self.open_indexes = s


def accordion(items: list[tuple[str, str]], allow_multiple: bool = True):
    def item(q: str, a: str, i: int):
        return rx.box(
            rx.button(
                q,
                on_click=lambda _=None, i=i: _AccordionState.toggle(i),
                class_name="w-full text-left font-medium flex justify-between items-center px-4 py-3 rounded-md bg-[var(--bg-soft)] hover:bg-[var(--primary-soft)] transition",
            ),
            rx.cond(
                lambda i=i: i in _AccordionState.open_indexes,
                rx.box(rx.text(a, class_name="content text-sm px-4 pb-4 pt-1"), class_name="fade-in"),
                rx.box(),
            ),
            class_name="border border-[var(--border-color)] rounded-lg"
        )

    return section(
        container(
            rx.vstack(
                *[item(q, a, i) for i, (q, a) in enumerate(items)],
                spacing="3",
            )
        )
    )
