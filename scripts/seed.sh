#!/bin/sh

set -e
set -o pipefail

echo "\n> Migrate (Refresh) and Seed test data"
docker exec -it barrows-app python seeder.py
echo "\n> Seeding completed"