"""Archivo raíz legado. La app principal está en ERC/ con nombre de paquete 'ERC'.

Se mantiene vacío para evitar doble instancia rx.App que causa errores en compilación.
"""

# Si se necesita compatibilidad, reexportar la app del paquete principal:
from ERC.ERC import app  # type: ignore  # noqa: F401

# Registro sencillo de endpoints API (REST-like)
if app._api:  # tipo: ignore
    app._api.add_route("/api/pacientes", listar_pacientes, methods=["GET"])  # tipo: ignore
    app._api.add_route("/api/pacientes", crear_paciente, methods=["POST"])  # tipo: ignore
