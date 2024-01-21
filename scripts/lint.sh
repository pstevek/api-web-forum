#!/bin/sh

set -e
set -o pipefail

echo "\n> Linting API with Ruff"
docker exec -it barrows-app ruff check --fix .
echo "\n> Done !"
