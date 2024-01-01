#!/bin/sh

set -e

echo "Seeding tables"
docker exec -it barrows-app python seeder.py
echo "Seeding completed"