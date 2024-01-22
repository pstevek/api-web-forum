#!/bin/sh

set -e
set -o pipefail

echo "\n> Running Test suite\n"
docker exec -it barrows-app /bin/sh -c "TEST_MODE=true && python -m pytest --disable-warnings"
echo "\n> Completed !"