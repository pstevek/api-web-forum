#!/bin/sh

set -e
set -o pipefail

echo "\n> Running Test suite\n"
docker exec -it forum-api /bin/sh -c "TEST_MODE=true && python -m pytest --disable-warnings"
echo "\n> Completed !"