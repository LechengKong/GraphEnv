# sp-haiku55-1 / hidden-pattern-probe__h5t79Ht

model=bedrock/us.anthropic.claude-haiku-5-5 reward=0.0 exception=None evaluate=78 best=0.9161

```bash
probe --help; echo ---; probe status
```

```bash
probe neighbors b8926eb97b
```

```bash
for n in 40234ca2ac 7177bc61e3 91b3c0bda3 e6f6a117af; do probe neighbors $n; done
```

```bash
cd /tmp && cat > bfs.sh <<'EOF'
#!/bin/bash
declare -A seen
queue=("$1")
seen["$1"]=1
depth_limit=${2:-4}
declare -A depth
depth["$1"]=0
out=""
while [ ${#queue[@]} -gt 0 ]; do
  cur=${queue[0]}; queue=("${queue[@]:1}")
  res=$(probe neighbors "$cur")
  echo "$res"
  d=${depth[$cur]}
  if [ $d -ge $depth_limit ]; then continue; fi
  for nb in $(echo "$res" | python3 -c 'import sys,json; print(" ".join(json.load(sys.stdin)["neighbors"]))'); do
    if [ -z "${seen[$nb]}" ]; then seen[$nb]=1; depth[$nb]=$((d+1)); queue+=("$nb"); fi
  done
done
EOF
bash bfs.sh b8926eb97b 6 > /tmp/graph.jsonl; wc -
```

```bash
cd /tmp && probe evaluate b8926eb97b; echo; probe evaluate b8926eb97b 40234ca2ac 7177bc61e3 91b3c0bda3 e6f6a117af; echo; probe evaluate 40234ca2ac
```

```bash
cd /tmp && for x in 7177bc61e3 91b3c0bda3 e6f6a117af 02ac8fd827 aaf16439e9; do probe evaluate $x; echo; done
```

```bash
cd /tmp && probe evaluate b8926eb97b 40234ca2ac; echo; probe evaluate 40234ca2ac 7177bc61e3; echo; probe evaluate 7ef4e009b3; echo; probe evaluate 1e6c93952f
```

```bash
cd /tmp && probe evaluate b8926eb97b; echo; probe evaluate 91b3c0bda3 b8926eb97b; echo; probe evaluate 40234ca2ac 7177bc61e3 91b3c0bda3 e6f6a117af b8926eb97b 02ac8fd827; echo
```

```bash
cd /tmp && python3 -I -c '
import json
g={}
for l in open("/tmp/graph.jsonl"):
    d=json.loads(l); g[d["node"]]=set(d["neighbors"])
allnodes=set(g)|set().union(*g.values())
print(len(g), len(allnodes), sorted(allnodes-set(g)))
# symmetry check
bad=[(a,b) for a in g for b in g[a] if b in g and a not in g[b]]
print("asym",bad[:5])
'
```

```bash
cd /tmp && for n in 067dea0198 0d913bd397 131932f0f8 1694914ac5 1f9ca1a684 3a25f48909 4a2417502e 58bb88d1b7 74c42287dd 763a294025 8154acc8eb 90f37b9031 aafcf5e45b ab27d4ab66 b35671addb b39ab09067 bd1299f7e7 c0fa0b3649 cfca3fb09c d5b21e9b48 d8063f3ab3 e1f76c1dc6 e6fe18ec41 e978719304 fb052d75c1; do probe neighbors $n; echo; done > /tmp/frontier.jsonl; python3 -I -c '
import json
g={}
for f in ["/tmp/graph.jsonl","/tmp/frontier.jsonl"]:
    for l in open(f):
        l=l.strip()
        if not l: continue
        d=json.loads(l); g[d["node"]]=set(d["neighbors"])
allnodes=set(g)|set().union(*g.val
```

```bash
mkdir -p /tmp/probe_work && cat > /tmp/probe_work/crawl.py <<'EOF'
import json, subprocess
g = json.load(open("/tmp/g.json"))
start = "b8926eb97b"
todo = [n for n in set().union(*map(set, g.values())) if n not in g]
while todo:
    n = todo.pop()
    if n in g: continue
    out = subprocess.run(["probe", "neighbors", n], capture_output=True, text=True).stdout
    nb = json.loads(out)["neighbors"]
    g[n] = sorted(nb)
    for m in nb:
        if m not in g: todo.append(m)
json.dump(g, open("/tmp/g.json", "w"))
allnodes = set(g) | set().union(*map(set, g.values()))
print("crawled", len(g), "tot
```

```bash
cd /tmp && python3 -I -c '
import json, collections
g={k:v for k,v in json.load(open("/tmp/g.json")).items()}
s="b8926eb97b"
dist={s:0}; q=[s]
for u in q:
    for v in g.get(u,[]):
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
print(collections.Counter(dist.values()))
deg=collections.Counter(len(v) for v in g.values())
print("deg dist", sorted(deg.items())[:20], "start deg", len(g[s]))
for x in ["40234ca2ac","7177bc61e3","91b3c0bda3","e6f6a117af","02ac8fd827","aaf16439e9","7ef4e009b3","1e6c93952f"]:
    print(x, dist.get(x), len(g[x]))
'
```

```bash
cd /tmp && python3 -I -c '
import json
g=json.load(open("/tmp/g.json")); s="b8926eb97b"
dist={s:0}; q=[s]
for u in q:
    for v in g[u]:
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
far=[k for k in dist if dist[k]==30][:1]+[k for k in dist if dist[k]==10][:1]
print(far)
open("/tmp/probe_work/far.txt","w").write(" ".join(far))
'; probe evaluate $(cut -d' ' -f1 /tmp/probe_work/far.txt); echo; probe evaluate $(cut -d' ' -f2 /tmp/probe_work/far.txt)
```

```bash
cd /tmp && probe evaluate b8926eb97b 7c68283178; echo; probe evaluate b8926eb97b 02ac8fd827; echo; probe evaluate b8926eb97b 7ef4e009b3; echo; probe evaluate b8926eb97b 40234ca2ac 91b3c0bda3; echo
```

```bash
cd /tmp && probe evaluate b8926eb97b 7c68283178 bd9ff23567; echo; probe evaluate 7c68283178 bd9ff23567; echo; probe evaluate b8926eb97b 40234ca2ac 7c68283178; echo
```

```bash
cd /tmp/probe_work && python3 -I -c '
import json
g=json.load(open("/tmp/g.json")); s="b8926eb97b"
dist={s:0}; q=[s]
for u in q:
    for v in g[u]:
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
for r in [1,2,3]:
    ball=[k for k in dist if dist[k]<=r]
    open(f"ball{r}.txt","w").write("\n".join(ball))
    print("ball",r,len(ball))
sph=[k for k in dist if dist[k]==2]; open("sph2.txt","w").write("\n".join(sph)); print("sph2",len(sph))
sph=[k for k in dist if dist[k]==3]; open("sph3.txt","w").write("\n".join(sph)); print("sph3",len(sph))
'; probe evaluate - < ball2.txt; echo; probe e
```

```bash
cd /tmp/probe_work && probe evaluate - < ball3.txt; echo; probe evaluate - < sph3.txt; echo
```

```bash
cd /tmp/probe_work && python3 -I -c '
import json
g=json.load(open("/tmp/g.json")); s="b8926eb97b"
dist={s:0}; q=[s]
for u in q:
    for v in g[u]:
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
for r in [4,5]:
    ball=[k for k in dist if dist[k]<=r]
    open(f"ball{r}.txt","w").write("\n".join(ball)); print(r,len(ball))
'; probe evaluate - < ball4.txt; echo
```

```bash
cd /tmp/probe_work && cat > toggle.py <<'EOF'
import json, subprocess
g=json.load(open("/tmp/g.json")); s="b8926eb97b"
dist={s:0}; q=[s]
for u in q:
    for v in g[u]:
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
b3=[k for k in dist if dist[k]<=3]
d4=[k for k in dist if dist[k]==4]
def ev(sel):
    out=subprocess.run(["probe","evaluate",*sel],capture_output=True,text=True)
    return json.loads(out.stdout)["score"]
res={}
for x in b3:
    res[("minus",x,dist[x])]=ev([y for y in b3 if y!=x])
for x in d4:
    res[("plus",x,dist[x])]=ev(b3+[x])
for k,v in sorted(res.items(), key=lambd
```

```bash
cd /tmp/probe_work && python3 -I -c '
import json
g=json.load(open("/tmp/g.json")); s="b8926eb97b"
dist={s:0}; q=[s]
for u in q:
    for v in g[u]:
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
open("ball3_nos.txt","w").write("\n".join(k for k in dist if 1<=dist[k]<=3))
open("ball2_nos.txt","w").write("\n".join(k for k in dist if 1<=dist[k]<=2))
'; probe evaluate - < ball3_nos.txt; echo; probe evaluate - < ball2_nos.txt; echo
```

```bash
cd /tmp/probe_work && python3 -I -c '
import json, collections
g=json.load(open("/tmp/g.json")); s="b8926eb97b"
N=set(g[s])
cn=collections.Counter()
for u in g:
    if u==s: continue
    c=len(set(g[u])&N)
    if c: cn[(c)]+=1
print("common-neighbor count distribution among nodes:", sorted(cn.items()))
for u in g[s]: print(u, len(g[u]), [ (v,len(set(g[v])&set(g[s]))) for v in g[u] if v!=s][:6])
# triangle count per node
tri={u: sum(1 for a in g[u] for b in g[u] if a<b and b in g[a]) for u in g}
print("tri(s)",tri[s], "avg tri", sum(tri.values())/len(tri))
'
```

```bash
cd /tmp/probe_work && python3 -I -c '
import json
g=json.load(open("/tmp/g.json")); s="b8926eb97b"
dist={s:0}; q=[s]
for u in q:
    for v in g[u]:
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
b3=[k for k in dist if dist[k]<=3]
e1=[k for k in b3 if k not in ("491b1446f4","7177bc61e3","40234ca2ac")]
open("e1.txt","w").write("\n".join(e1)); print(len(e1))
'; probe evaluate - < e1.txt
```

```bash
cd /tmp/probe_work && python3 -I -c '
import json, collections
g=json.load(open("/tmp/g.json")); s="b8926eb97b"
asym=[(a,b) for a in g for b in g[a] if a not in g.get(b,[])]
print("asymmetric arcs:", len(asym))
print("nodes w/ self loop", sum(1 for a in g if a in g[a]))
dist={s:0}; q=[s]
for u in q:
    for v in g[u]:
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
print("ecc of start", max(dist.values()))
tri=sum(1 for a in g for b in g[a] for c in g[b] if c in g[a] and a<b<c)
print("triangles", tri)
'
```

```bash
cd /tmp/probe_work && probe evaluate 40234ca2ac b8926eb97b; echo; probe evaluate 7177bc61e3 b8926eb97b 40234ca2ac; echo
```

```bash
cd /tmp/probe_work && probe evaluate b8926eb97b 0d66623d41 aaf16439e9 58f1750432 f5627a7cb1
```

```bash
cd /tmp/probe_work && python3 -I -c '
import json, collections
g=json.load(open("/tmp/g.json")); s="b8926eb97b"
def comp(allowed):
    if s not in allowed: return None
    seen={s}; q=[s]
    for u in q:
        for v in g[u]:
            if v in allowed and v not in seen: seen.add(v); q.append(v)
    return seen
cands={}
for lo,hi in [(2,5),(2,4),(3,5),(3,4),(1,4),(2,6),(3,6),(1,5)]:
    A={u for u in g if lo<=len(g[u])<=hi}
    c=comp(A); cands[f"deg{lo}-{hi}"]=None if c is None else len(c)
print(cands)
# k-core
def kcore(k):
    alive=set(g)
    ch=True
    while ch:
        ch=False
      
```

```bash
cd /tmp/probe_work && python3 -I -c '
import json
g=json.load(open("/tmp/g.json")); s="b8926eb97b"
dist={s:0}; q=[s]
for u in q:
    for v in g[u]:
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
b3=[k for k in dist if dist[k]<=3]
open("e2.txt","w").write("\n".join(b3+["a2a357bf60","4cb0aae75d","d0fae90990"]))
'; probe evaluate - < e2.txt
```

```bash
cd /tmp/probe_work && probe submit - < e2.txt; echo; probe status
```

**agent:** I submitted a 29-item selection, but I could not confirm that it matches the target. It is the best-scoring candidate I found, not a verified answer, and I expect it is probably not an exact match.

**What I submitted:** the start item's 3-hop ball (26 items) plus three distance-4 items (`a2a357bf60`, `4cb0aae75d`, `d0fae90990`). It scored 0.9149, the highest of any selection containing the start item that I tested.

**What I established:**
- The graph is one connected component of 1,599 items and 2,934 undirected links. The start item's eccentricity is 47.
- Scores for the candidate rules I tested were all below 1.0:
  - Start plus its neighbours (5 items): 0.4066
  - 2-hop ball (13 items): 0.833
  - 3-hop ball (26 items): 0.9024
  - 4-hop ball (42 items): 0.8952
  - Start plus items sharing two links with it (5 items): 0.4066
- Scores seem to depend on membership in a way I could not model. Every single non-start item scored the same 0.4154, and removing one node sometimes raised the score while removing three of them together lowered it. Because of this, I could not reverse-engineer the scoring formula, and I could not infer the target from the scores.

**What I did not establish:** the rule that defines the target. I checked several simple candidates (balls, spheres, common-neighbour sets). None scored 1.0, and I did not test degree-based or k-core rules beyond computing their sizes. The submission was chosen by score, not by a confirmed rule.

Budget: 78 of 150 `evaluate` calls used. The submission is final, so the task is closed.

