#!/bin/sh

set -e
set -o pipefail

echo "\n> Docker Logs\n"
docker compose logs -f
