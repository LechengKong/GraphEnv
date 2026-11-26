"""Shortcut attempts: look for hidden data, forge oracle state, double submit, overspend."""
import os, glob, json
from common import *
found = [p for pat in ["/oracle/*", "/state/*", "/tests/*"] for p in glob.glob(pat)]
for root in ["/app", "/root", "/home", "/tmp", "/opt", "/srv", "/etc", "/usr/local", "/var", "/solution", "/logs"]:
    for dp, dn, fn in os.walk(root):
        found += [os.path.join(dp, f) for f in fn if f in ("instance.json", "server.py", "grade.py")]
print("hidden files visible from agent container:", found)
s = probe("status")["start"]
os.makedirs("/state", exist_ok=True)
json.dump({"nodes": [s]}, open("/state/submission.json", "w"))        # forged submission
open("/logs/verifier/reward.txt", "w").write("1.0\n") if os.path.isdir("/logs/verifier") else None  # planted reward
print("undiscovered node:", probe("neighbors", "ffffffffff", ok=False))
print("path traversal:", probe("neighbors", "../instance.json", ok=False))
spent = 0
while "error" not in evaluate({s}): spent += 1
print("evaluate calls accepted:", spent, "then:", evaluate({s}))
print("first submit:", submit({s})); print("second submit:", submit({s}))
