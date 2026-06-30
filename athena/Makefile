.PHONY: install test lint clean deps-check codegen graph docs

VENV := athena-core/.venv
PY := $(VENV)/Scripts/python
PIP := $(VENV)/Scripts/pip

ifeq ($(OS),Windows_NT)
else
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
endif

PACKAGES := athena-os athena-common athena-domain athena-core \
	athena-data athena-indicators athena-patterns athena-strategies \
	athena-risk athena-portfolio athena-execution athena-math athena-research \
	athena-platform athena-sdk athena-ai athena-cli athena-dashboard athena-testing

install:
	cd athena-core && python -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -e "../athena-os[dev]"
	$(PIP) install -e "../athena-common[dev]"
	$(PIP) install -e "../athena-domain[dev]"
	$(PIP) install -e ".[dev]"
	$(PIP) install -e "../athena-data[dev]" -e "../athena-indicators[dev]" \
		-e "../athena-patterns[dev]" -e "../athena-strategies[dev]" \
		-e "../athena-risk[dev]" -e "../athena-portfolio[dev]" \
		-e "../athena-execution[dev]" -e "../athena-math[dev]" \
		-e "../athena-research[dev]" -e "../athena-platform[dev]"
	$(PIP) install -e "../athena-sdk[dev]" -e "../athena-ai[dev]" -e "../athena-cli[dev]" -e "../athena-dashboard[dev]"
	$(PIP) install -e "../athena-testing[dev]"

# Hatch editable installs leave stale shadow dirs if force-reinstall was used; remove them.
	-$(PY) -c "from pathlib import Path; sp=Path('$(VENV)/Lib/site-packages'); [__import__('shutil').rmtree(sp/n, ignore_errors=True) for n in ('athena_core','athena_os','athena_common') if (sp/f'_editable_impl_{n}.pth').exists() and (sp/n).is_dir()]"

test:
	cd athena-os && ../athena-core/$(PY) -m pytest -q
	cd athena-common && ../athena-core/$(PY) -m pytest -q
	cd athena-domain && ../athena-core/$(PY) -m pytest -q
	cd athena-core && $(PY) -m pytest -q
	cd athena-data && ../athena-core/$(PY) -m pytest -q
	cd athena-indicators && ../athena-core/$(PY) -m pytest -q
	cd athena-patterns && ../athena-core/$(PY) -m pytest -q
	cd athena-strategies && ../athena-core/$(PY) -m pytest -q
	cd athena-risk && ../athena-core/$(PY) -m pytest -q
	cd athena-portfolio && ../athena-core/$(PY) -m pytest -q
	cd athena-execution && ../athena-core/$(PY) -m pytest -q
	cd athena-math && ../athena-core/$(PY) -m pytest -q
	cd athena-research && ../athena-core/$(PY) -m pytest -q
	cd athena-platform && ../athena-core/$(PY) -m pytest -q
	cd athena-sdk && ../athena-core/$(PY) -m pytest -q
	cd athena-ai && ../athena-core/$(PY) -m pytest -q
	cd athena-cli && ../athena-core/$(PY) -m pytest -q
	cd athena-dashboard && ../athena-core/$(PY) -m pytest -q
	cd athena-testing && ../athena-core/$(PY) -m pytest -q

deps-check:
	$(PY) scripts/check_dependencies.py

codegen:
	$(PY) scripts/generate_events.py

graph:
	$(PY) scripts/generate_dependency_graph.py --dot

docs:
	$(PY) scripts/generate_docs.py

lint:
	cd athena-core && $(PY) -m ruff check src tests

clean:
	rm -rf athena-core/.venv
