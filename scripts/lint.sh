#!/bin/sh

set -e
set -o pipefail

echo "\n> Linting API with Ruff"
docker exec -it forum-api ruff check --fix .
echo "\n> Done !"
