#!/bin/sh

set -e
set -o pipefail

echo "\n> Run Migrations and Seeders"
docker exec -it barrows-app python seeder.py
echo "\n> Migration and Seeding completed !"