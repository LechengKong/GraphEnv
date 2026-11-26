#!/bin/bash
# Usage: tools/run_harbor.sh <job-name> <harbor run args...>   (run on a compute node)
set -uo pipefail
export PATH=$HOME/.local/bin:$PATH
cd "$(dirname "$0")/.."
name=$1; shift
harbor run -p "${TASK:-tasks/hidden-pattern-probe}" -o jobs --job-name "$name" -y "$@"
