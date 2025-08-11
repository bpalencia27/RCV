# Dockerfile inicial PR1 (Reflex + FastAPI)
FROM python:3.11.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema mínimas (añadir si parser PDF requiere más)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./

# Instalar dependencias (usar pip directamente hasta definir build)
RUN pip install --upgrade pip && \
    pip install .[dev]

COPY rcvco ./rcvco
COPY assets ./assets
COPY app.py ./app.py
COPY rxconfig.py ./rxconfig.py

EXPOSE 8000

# Comando: lanzar Reflex (que internamente sirve API)
CMD ["python", "-m", "reflex", "run", "--env", "prod"]
