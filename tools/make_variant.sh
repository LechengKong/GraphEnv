#!/bin/bash
# Clone the task with a negative attempt as its "solution": tools/make_variant.sh <name>
set -euo pipefail
cd "$(dirname "$0")/.."
dst=jobs/variants/$1; rm -rf "$dst"; mkdir -p jobs/variants
cp -r tasks/hidden-pattern-probe "$dst"; rm -rf "$dst/solution"; mkdir "$dst/solution"
cp tools/negatives/common.py tools/negatives/$1/* "$dst/solution/"
echo "$dst"
