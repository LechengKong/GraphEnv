"""Print the agent's visible text and bash commands from a Harbor trajectory.json (compact)."""
import json, sys
t = json.load(open(sys.argv[1]))
steps = t.get("steps", t if isinstance(t, list) else [])
for st in steps:
    src = st.get("source")
    if src != "agent":
        continue
    msg = (st.get("message") or "").strip()
    if msg:
        print("TEXT:", msg[:int(sys.argv[2]) if len(sys.argv) > 2 else 400].replace("\n", " "))
    for tc in st.get("tool_calls") or []:
        a = tc.get("arguments") or {}
        cmd = a.get("command") or a.get("content") or json.dumps(a)
        print("  $", str(cmd)[:160].replace("\n", " ⏎ "))
