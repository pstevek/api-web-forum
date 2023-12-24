#!/bin/sh

set -e

echo "Seeding tables"
docker exec -it barrows-db psql -U postgres -d barrows -f /tmp/data.sql
echo "Seeding completed"