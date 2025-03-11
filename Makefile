#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = PhantomBusterDiscovery
PYTHON_VERSION = 3.11

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Create/Update the project's environment
.PHONY: sync
sync:
	uv sync

## Format source code
.PHONY: format
format:
	ruff format

## Check source code
.PHONY: check
check:
	ruff check --fix

## Download data
.PHONY: download-data
download-data:
	uv run src/data/get-data.py

## Build databases
.PHONY: build-databases
build-databases:
	uv run src/data/feed-structured-db.py
	uv run src/data/feed-vector-db.py

## Serve UI
.PHONY: serve-ui
serve-ui:
	uv run chainlit run app.py -w

		
#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
