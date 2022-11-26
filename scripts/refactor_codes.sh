#!/usr/bin/env bash

CURRENT_SCRIPT="$(basename -- "$0")"
SCRIPT_DIRNAME="$(dirname -- "$0")"
PROJECT_ROOT="$(dirname "$SCRIPT_DIRNAME")"

echo "[Removing unused Python imports]"
autoflake --remove-all-unused-imports -i -r "$PROJECT_ROOT"
echo "[Reformatting Python codes]"
black "$PROJECT_ROOT"