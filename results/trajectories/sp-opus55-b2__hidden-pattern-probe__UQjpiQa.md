# sp-opus55-b2 / hidden-pattern-probe__UQjpiQa

model=bedrock/us.anthropic.claude-opus-5-5 reward=0.0 exception=None evaluate=150 best=0.9498

```bash
probe --help; probe status
```

**agent:** Let me crawl the graph (neighbors is free).

```bash
cd /tmp && cat > crawl.py <<'EOF'
import json,subprocess,collections
s="b8926eb97b"
adj={};dist={s:0};q=collections.deque([s])
while q:
    u=q.popleft()
    out=json.loads(subprocess.run(["probe","neighbors",u],capture_output=True,text=True).stdout)
    adj[u]=out
    if len(adj)>5000: break
    for v in (out if isinstance(out,list) else out.get("neighbors",[])):
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
json.dump({"adj":adj,"dist":dist},open("g.json","w"))
print(len(adj),collections.Counter(dist.values()))
print(json.dumps(adj[s])[:500])
EOF
python3 crawl.py
```

```bash
cd /tmp && python3 -c "
import json,collections
g=json.load(open('g.json'));adj={k:v['neighbors'] for k,v in g['adj'].items()}
asym=sum(1 for u in adj for v in adj[u] if u not in adj.get(v,[]))
print('asym',asym, collections.Counter(len(v) for v in adj.values()))
"
for k in 0 1 2 3; do python3 -c "
import json;g=json.load(open('/tmp/g.json'));print('\n'.join(x for x,d in g['dist'].items() if d<=$k))" | probe evaluate -; done
```

```bash
cd /tmp; for k in 4 5 6; do python3 -c "
import json;g=json.load(open('/tmp/g.json'));print('\n'.join(x for x,d in g['dist'].items() if d<=$k))" | probe evaluate -; done
```

```bash
cd /tmp && cat > ev.py <<'EOF'
import json,subprocess,sys
g=json.load(open('/tmp/g.json'));adj={k:v['neighbors'] for k,v in g['adj'].items()};dist=g['dist']
def ev(S):
    r=subprocess.run(["probe","evaluate","-"],input="\n".join(S),capture_output=True,text=True).stdout
    return json.loads(r)["score"]
EOF
python3 -c "
exec(open('/tmp/ev.py').read())
B=[x for x,d in dist.items() if d<=5]
s5=[x for x in B if dist[x]==5]; s1=[x for x in B if dist[x]==1]
print(ev([x for x in B if x!=s5[0]]), ev([x for x in B if x!=s1[0]]))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
B=lambda f:[x for x,d in dist.items() if f(d)]
print(ev(B(lambda d:d<=3 or d==5)))
print(ev(B(lambda d:d<=2 or d==5 or d==4)))
print(ev(B(lambda d:d<=4 and d!=1)))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
B=[x for x,d in dist.items() if d<=5]; base=0.9339
res={}
for x in B:
    res[x]=ev([y for y in B if y!=x])-base
json.dump(res,open('/tmp/rem.json','w'))
for x in sorted(res,key=res.get): print(x,dist[x],len(adj[x]),round(res[x],4))
"
```

**agent:** Ball of radius 5 scores 0.934. Single-node removals have small, non-additive effects, so the score is not plain set overlap. Next I'll test removing every node whose removal raised the score.

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
res=json.load(open('/tmp/rem.json'));B=list(res)
print(len(B))
for t in [0.005,0.002,0.0]:
    S=[x for x in B if res[x]<=t]; print(t,len(S),ev(S))
"
```

```bash
cd /tmp && cat > hyp.py <<'EOF'
import json
exec(open('/tmp/ev.py').read())
res=json.load(open('/tmp/rem.json'))
B5=[x for x,d in dist.items() if d<=5]
obs=[]
for k,s in zip(range(7),[0.0148,0.4066,0.833,0.9024,0.8952,0.9339,0.9096]):
    obs.append(([x for x,d in dist.items() if d<=k],s))
for x,v in res.items(): obs.append(([y for y in B5 if y!=x],0.9339+v))
def J(a,b): a,b=set(a),set(b); return len(a&b)/len(a|b) if a|b else 1
def closed(S): s=set(S); [s.update(adj[x]) for x in S]; return s
def inc(S): return {frozenset((x,y)) for x in S for y in adj[x]}
def ind(S): s=set(S); return {frozense
```

```bash
cd /tmp && cat > cand.py <<'EOF'
import json,collections
exec(open('/tmp/ev.py').read())
s="b8926eb97b"; deg={x:len(adj[x]) for x in adj}
def ball(ok,k=99):
    if not ok(s): return None
    D={s:0};q=collections.deque([s])
    while q:
        u=q.popleft()
        if D[u]>=k: continue
        for v in adj[u]:
            if v not in D and ok(v): D[v]=D[u]+1;q.append(v)
    return sorted(D)
C={}
for name,ok in [('ge3',lambda x:deg[x]>=3),('ge4',lambda x:deg[x]>=4),('le4',lambda x:deg[x]<=4),('le5',lambda x:deg[x]<=5),('eq4',lambda x:deg[x]==4),('in34',lambda x:3<=deg[x]<=4),('ge2',lambda x:de
```

**agent:** Every set near the start scores around 0.9, even a 10-node one (0.78), so this metric is very forgiving. Before trying more rules I'll measure its shape on single nodes at different distances.

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
by={}
for x,d in dist.items(): by.setdefault(d,[]).append(x)
for d in [1,3,5,8,20]: print(d, ev([by[d][0]]))
print('start+far', ev(['b8926eb97b',by[20][0]]))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
by={}
for x,d in dist.items(): by.setdefault(d,[]).append(x)
print('2far', ev([by[20][0],by[30][0]]))
print('2near', ev(by[1][:2]))
print('ball1-start', ev(by[1]))
print('5far', ev(by[30][:5]))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
by={}
for x,d in dist.items(): by.setdefault(d,[]).append(x)
print('20far', ev(by[30][:20]))
print('60far', ev(by[20][:30]+by[21][:30]))
print('start+nb', ev(['b8926eb97b',by[1][0]]))
print('ball2-start', ev(by[1]+by[2]))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
import random
random.seed(1)
allx=[x for x in dist if x!='b8926eb97b']
for k in [20,60]:
    print(k,'scatter',ev(random.sample(allx,k)))
# connected ball around far node
far=[x for x,d in dist.items() if d==30][0]
D={far:0};q=[far]
while len(D)<60:
    u=q.pop(0)
    for v in adj[u]:
        if v not in D: D[v]=1;q.append(v)
print('60 far ball',ev(list(D)[:60]))
"
```

```bash
cd /tmp && pip list 2>/dev/null | grep -i networkx; python3 -c "
import json,networkx as nx
g=json.load(open('/tmp/g.json'));G=nx.Graph()
for k,v in g['adj'].items():
    for y in v['neighbors']: G.add_edge(k,y)
s='b8926eb97b'
print(G.number_of_nodes(),G.number_of_edges(),'tri',sum(nx.triangles(G).values())//3)
cn=nx.core_number(G);print('core',cn[s],max(cn.values()))
for k in range(1,max(cn.values())+1):
    H=G.subgraph([x for x in G if cn[x]>=k]); 
    if s in H: print(k,len(nx.node_connected_component(H,s)))
bl=[b for b in nx.biconnected_components(G) if s in b];print('blocks',[len(b) for 
```

```bash
cd /tmp && cat > com.py <<'EOF'
import json,networkx as nx
exec(open('/tmp/ev.py').read())
G=nx.Graph()
for k,v in adj.items():
    for y in v: G.add_edge(k,y)
s='b8926eb97b'
seen=set()
for r in [0.5,1,2,4]:
  for seed in [0,1]:
    cs=nx.community.louvain_communities(G,resolution=r,seed=seed)
    c=[c for c in cs if s in c][0]
    key=frozenset(c)
    if key in seen or len(c)>200: print(r,seed,len(c),'skip');continue
    seen.add(key); print(r,seed,len(c),ev(sorted(c)))
EOF
python3 com.py
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
s='b8926eb97b'
by={}
for x,d in dist.items(): by.setdefault(d,[]).append(x)
a=by[30][0]; b=adj[a][0]; c=[y for y in adj[b] if y!=a][0]
n1=adj[s][0]; n2=adj[s][1]
print('edge far',ev([a,b]))
print('path3 far',ev([a,b,c]))
print('s+2far',ev([s,by[20][0],by[25][0]]))
print('s+n1+n2',ev([s,n1,n2]))
print('s+edgefar',ev([s,a,b]))
"
```

```bash
cd /tmp && cat > motif.py <<'EOF'
import json,networkx as nx
exec(open('/tmp/ev.py').read())
from networkx.algorithms import isomorphism as iso
G=nx.Graph()
for k,v in adj.items():
    for y in v: G.add_edge(k,y)
far=[x for x,d in dist.items() if d>=25]
def find(P):
    H=G.subgraph(far)
    GM=iso.GraphMatcher(H,P)
    for m in GM.subgraph_isomorphisms_iter():  # induced
        return list(m.keys())
import sys
mot={'star3':nx.star_graph(3),'star4':nx.star_graph(4),'path4':nx.path_graph(4),'path5':nx.path_graph(5),'tri':nx.cycle_graph(3),'sq':nx.cycle_graph(4)}
for n,P in mot.items():
    S=f
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
s='b8926eb97b'
D={}
for x in adj:
    if x!=s and dist[x]>10: D.setdefault(len(adj[x]),x)
print({d:ev([x]) for d,x in sorted(D.items())})
"
```

```bash
cd /tmp && cat > fit.py <<'EOF'
import json,networkx as nx,numpy as np,collections
from networkx.algorithms import isomorphism as iso
g=json.load(open('/tmp/g.json'));adj={k:v['neighbors'] for k,v in g['adj'].items()};dist=g['dist']
G=nx.Graph()
for k,v in adj.items():
    for y in v: G.add_edge(k,y)
s='b8926eb97b'
by={}
for x,d in dist.items(): by.setdefault(d,[]).append(x)
far=[x for x,d in dist.items() if d>=25]
def find(P):
    for m in iso.GraphMatcher(G.subgraph(far),P).subgraph_isomorphisms_iter(): return list(m.keys())
a=by[30][0]; b=adj[a][0]; c=[y for y in adj[b] if y!=a][0]
obs=[([b
```

**agent:** Pair-distance features don't fit either; the residuals are large. More controlled probes: mixing a path of 3 with isolated nodes and with extra disjoint edges.

```bash
cd /tmp && cat > p2.py <<'EOF'
exec(open('/tmp/ev.py').read())
import networkx as nx
from networkx.algorithms import isomorphism as iso
G=nx.Graph()
for k,v in adj.items():
    for y in v: G.add_edge(k,y)
by={}
for x,d in dist.items(): by.setdefault(d,[]).append(x)
a=by[30][0]; b=adj[a][0]; c=[y for y in adj[b] if y!=a][0]
P3=[a,b,c]
iso_far=[x for x in by[40][:]][:6]
# check isolation
print([sum(1 for y in adj[x] if y in set(iso_far+P3)) for x in iso_far])
print('P3+1iso',ev(P3+iso_far[:1]))
print('P3+3iso',ev(P3+iso_far[:3]))
# two disjoint edges far
e2=[by[35][0],adj[by[35][0]][0]]
print('2
```

```bash
cd /tmp && cat > p3.py <<'EOF'
exec(open('/tmp/ev.py').read())
import networkx as nx
from networkx.algorithms import isomorphism as iso
G=nx.Graph()
for k,v in adj.items():
    for y in v: G.add_edge(k,y)
P=nx.path_graph(3);out=[]
for d in [3,10,40]:
    reg=[x for x,dd in dist.items() if abs(dd-d)<=2]
    for m in iso.GraphMatcher(G.subgraph(reg),P).subgraph_isomorphisms_iter():
        S=list(m.keys()); break
    out.append((d,ev(S)))
s='b8926eb97b'
nb=adj[s]
# star at start minus start: 4 nbrs + a node? ; ball1 of far deg4 node
x=[x for x,dd in dist.items() if dd==30 and len(adj[x])==4][0]

```

```bash
probe status; probe evaluate b8926eb97b
```

```bash
cd /tmp && python3 -c "
import json;g=json.load(open('/tmp/g.json'));print('\n'.join(x for x,d in g['dist'].items() if d<=5))" | probe submit -
```

**agent:** I submitted a guess, and it probably doesn't match the target: its best score was 0.9339, not 1.0. The submission was the 61 items within 5 links of the start item, and it was accepted.

**What I found:**
- The full system has 1,599 items and 2,934 links, all two-way. Running outward from the start item, it reaches distance 47.
- **The score barely depends on which items you pick.** Any single item other than the start scores 0.4154, wherever it is and however many links it has. The start alone scores only 0.0148. A connected group of 60 items far from the start scored 0.889, while 60 scattered items scored 0.436.
- **It depends on the shape of the selection instead.** That means size, how the chosen items link to each other, and whether the start is included. A cosine comparison of label counts fit some small cases exactly. Plain degree counts, pair distances and graph-level counts all failed to fit the other cases.
- **Nothing I tried reached 1.0:**

| Candidate | Score |
|---|---|
| Within 5 links of the start (submitted) | 0.9339 |
| Same, without the start item (excluded: the target must contain it) | 0.9383 |
| Community detection | 0.9404 |
| Within 7 links, only through items with at most 5 links (best overall) | 0.9476 |

I chose the radius-5 set because it is the most natural simple rule among the top scorers.

**What went wrong:** I ran out of evaluate calls by mistake. My batch scripts used them faster than I counted, and the single-item removal sweep alone took 61. I only noticed when a call failed with the budget at 150/150. That left me without calls to finish working out the scoring and without a confirmed 1.0. I should have tracked usage and spent the budget on decoding the scoring rule before sweeping item by item.

