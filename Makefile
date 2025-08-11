PY=python
PIP=$(PY) -m pip
APP_MODULE=rcvco.api.app:app

install:
	$(PIP) install -e .[dev]

format:
	$(PY) -m black .
	$(PY) -m ruff check --fix .

lint:
	$(PY) -m ruff check .
	$(PY) -m mypy rcvco

test:
	$(PY) -m pytest -q --cov=rcvco --cov-report=term-missing

run:
	$(PY) -m uvicorn $(APP_MODULE) --reload

e2e:
	@echo "(Placeholder) Ejecutar Playwright headless"

.PHONY: install format lint test run e2e
