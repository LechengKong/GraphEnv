#!/bin/bash
# Runs in a separate verifier container. /state is the oracle's state directory, collected
# from the oracle service after the agent finished; /tests/instance.json is the hidden instance.
mkdir -p /logs/verifier
python3 /tests/grade.py --state /state --instance /tests/instance.json --out /logs/verifier
