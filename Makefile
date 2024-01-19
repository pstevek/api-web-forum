.PHONY: help clean start lint test init-db logs

help:
	@echo "\n\t:: Command List ::\n"
	@echo "\tclean 	-- Detach and destroy all docker dependencies created"
	@echo "\tstart 	-- Start Docker network via Docker compose with all dependencies"
	@echo "\tlint 	-- Lint with style fixes with Ruff"
	@echo "\tlogs	-- Tail Docker logs"

clean:
	./scripts/clean.sh

start:
	./scripts/start.sh

lint:
	./scripts/lint.sh

seed:
	./scripts/seed.sh

logs:
	./scripts/logs.sh
