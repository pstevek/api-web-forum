.PHONY: help clean start lint test migrate logs

help:
	@echo "\n\t:: Command List ::\n"
	@echo "\tclean      -- Detach and destroy all docker dependencies created"
	@echo "\tstart      -- Start Docker network via Docker compose with all dependencies"
	@echo "\tlint       -- Lint with style fixes with Ruff"
	@echo "\ttest       -- Run test suite"
	@echo "\tmigrate    -- Run migrations and seeders"
	@echo "\tlogs       -- Tail Docker logs"

clean:
	./scripts/clean.sh

start:
	./scripts/start.sh

lint:
	./scripts/lint.sh

test:
	./scripts/test.sh

migrate:
	./scripts/migrate.sh

logs:
	./scripts/logs.sh
