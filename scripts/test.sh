#!/bin/sh

set -e
set -o pipefail

echo "\n> Running Test suite"
docker exec -it barrows-app /bin/sh -c "TEST_MODE=true && python -m pytest --disable-warnings"