import reflex as rx

config = rx.Config(
    app_name="RCV-CO",  # nombre más específico
    env=rx.Env.DEV,  # facilita desarrollo
    frontend_path="rcvco/ui",  # organización más clara
    api_url="/api",
    db_url="sqlite:///rcvco.db",  # db local para dev
    telemetry_enabled=False,  # sin datos de uso
    plugins=[
        rx.plugins.SitemapPlugin(),  # SEO
        rx.plugins.TailwindV4Plugin(  # UI moderna
            config={"darkMode": "class"}  # soporte dark mode
        ),
    ],
)
