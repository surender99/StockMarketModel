.PHONY: install test lint clean

VENV := athena-core/.venv
PY := $(VENV)/Scripts/python
PIP := $(VENV)/Scripts/pip

ifeq ($(OS),Windows_NT)
else
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
endif

install:
	cd athena-core && python -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -e "../athena-os[dev]"
	$(PIP) install -e ".[dev]"
	$(PIP) install -e "../athena-sdk[dev]" -e "../athena-ai[dev]" -e "../athena-cli[dev]" -e "../athena-dashboard[dev]"
	$(PIP) install -e "../athena-testing[dev]"

test:
	cd athena-os && ../athena-core/$(PY) -m pytest -q
	cd athena-core && $(PY) -m pytest -q
	cd athena-sdk && ../athena-core/$(PY) -m pytest -q
	cd athena-ai && ../athena-core/$(PY) -m pytest -q
	cd athena-cli && ../athena-core/$(PY) -m pytest -q
	cd athena-dashboard && ../athena-core/$(PY) -m pytest -q
	cd athena-testing && ../athena-core/$(PY) -m pytest -q

deps-check:
	$(PY) scripts/check_dependencies.py

lint:
	cd athena-core && $(PY) -m ruff check src tests

clean:
	rm -rf athena-core/.venv
