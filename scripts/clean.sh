#!/bin/sh

set -e
set -o pipefail

echo "\n> Destroy all Docker dependencies"
docker compose down --rmi all -v --remove-orphans
echo "\n> Environment variables clean up"
rm -rf .env
echo "\n> Remove all caching arterfacts"
find . | grep -E "(/__pycache__$|\.pytest_cache$|\.ruff_cache$|\.pyc$|\.pyo$)" | xargs rm -rf
echo "\n> Datastore / volumes clean up"
rm -rf data
rm -rf src/*.db
echo "\n> Clean up completed\n"
