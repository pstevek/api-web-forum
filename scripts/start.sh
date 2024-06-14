#!/bin/sh

set -e
set -o pipefail

echo "\n> Copy environment variables"
cp .env.sample .env
echo "\n> Startup docker compose network\n"
docker compose up -d --build
echo "\n> Docker network up and running\n"