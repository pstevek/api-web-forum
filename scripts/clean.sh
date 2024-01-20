#!/bin/sh

set -e
set -o pipefail

echo "\n> Destroy all Docker dependencies"
docker compose down --rmi all -v --remove-orphans
echo "\n> Environment variables clean up"
rm -f .env
echo "\n> Datastore / volumes clean up"
rm -rf data
echo "\n> Clean up completed\n"