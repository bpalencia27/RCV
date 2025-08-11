import reflex as rx, json

# Componente SEO mínimo sin romper el head global (se puede insertar al inicio de la página)

def seo_head(title: str, desc: str, url: str = "", image: str = "/static/og.png"):
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Plataforma Clínica",
        "url": url or "https://example.local",
    }
    return rx.fragment(
        rx.head(
            rx.title(title),
            rx.meta(name="description", content=desc),
            rx.meta(property="og:title", content=title),
            rx.meta(property="og:description", content=desc),
            rx.meta(property="og:type", content="website"),
            rx.meta(property="og:url", content=url),
            rx.meta(property="og:image", content=image),
            rx.meta(name="twitter:card", content="summary"),
            rx.meta(name="twitter:title", content=title),
            rx.meta(name="twitter:description", content=desc),
            rx.meta(name="twitter:image", content=image),
            rx.script(json.dumps(org), type_="application/ld+json"),
        )
    )
