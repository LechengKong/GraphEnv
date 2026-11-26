#!/bin/bash
# Usage: tools/run_agent.sh <job-name> <model> <n-trials>   (submit with sbatch)
set -uo pipefail
export PATH=$HOME/.local/bin:$PATH
cd "$(dirname "$0")/.."
eval "$(uv run -q --no-project --with boto3 python tools/aws_env.py)"
unset AWS_PROFILE
export CLAUDE_CODE_USE_BEDROCK=1 AWS_REGION=${AWS_REGION:-us-west-2}
harbor run -p "${TASK:-tasks/hidden-pattern-probe}" -o jobs --job-name "$1" -y \
  -a claude-code -m "bedrock/$2" -k "$3" -n "$3" --max-retries 2
