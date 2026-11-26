#!/bin/bash
set -euo pipefail
RULE=union2 python3 "$(dirname "$0")/solve.py"
