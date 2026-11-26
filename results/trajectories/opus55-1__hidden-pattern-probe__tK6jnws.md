# opus55-1 / hidden-pattern-probe__tK6jnws

model=bedrock/us.anthropic.claude-opus-5-5 reward=0.0 exception=AgentTimeoutError evaluate=86 best=0.9506

```bash
probe --help; probe status
```

**agent:** Let me BFS the graph fully (neighbors are free).

```bash
cd /tmp && cat > bfs.py <<'EOF'
import json,subprocess,collections
s="b8926eb97b"
adj={};dist={s:0};q=collections.deque([s])
while q:
    u=q.popleft()
    out=json.loads(subprocess.check_output(["probe","neighbors",u]))
    adj[u]=out
    for v in (out if isinstance(out,list) else out.get("neighbors",[])):
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
json.dump({"adj":adj,"dist":dist},open("g.json","w"))
print(len(dist),collections.Counter(dist.values()))
print(json.dumps(adj[s])[:500])
EOF
python3 bfs.py
```

```bash
cd /tmp && cat > ev.py <<'EOF'
import json,subprocess,sys
g=json.load(open("g.json"));d=g["dist"]
for k in map(int,sys.argv[1:]):
    sel=[x for x in d if d[x]<=k]
    if len(sel)>200: print(k,len(sel),"too big");continue
    r=subprocess.run(["probe","evaluate","-"],input="\n".join(sel),capture_output=True,text=True)
    print(k,len(sel),r.stdout,r.stderr)
EOF
python3 ev.py 0 1 2 3 4
```

```bash
cd /tmp && python3 -c "
import json,collections
g=json.load(open('g.json'));A={k:set(v['neighbors']) for k,v in g['adj'].items()};d=g['dist']
asym=sum(1 for u in A for v in A[u] if u not in A[v]);print('asym',asym)
print(collections.Counter(len(v) for v in A.values()))
for k in range(5):
  print(k,[ (x,len(A[x])) for x in d if d[x]==k])
"
```

```bash
cd /tmp && cat > tog.py <<'EOF'
import json,subprocess,sys
g=json.load(open("g.json"));d=g["dist"]
base=set(x for x in d if d[x]<=3)
def ev(s):
    r=subprocess.run(["probe","evaluate","-"],input="\n".join(s),capture_output=True,text=True)
    return json.loads(r.stdout)["score"]
for k in map(int,sys.argv[1:]):
    for x in [x for x in d if d[x]==k]:
        s=base^{x}
        print(k,x,ev(s),flush=True)
EOF
python3 tog.py 4
```

```bash
cd /tmp && python3 tog.py 3 2
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
base=set(x for x in d if d[x]<=3)
for x in '313c79969e 4cb0aae75d a2a357bf60 d0fae90990 4e9c76f251 543d7b8ed2 491b1446f4 9f24f98ecf 734d5f2a17 aaf16439e9 e7a1da5fa7 02ac8fd827'.split(): base^={x}
r=subprocess.run(['probe','evaluate','-'],input='\n'.join(base),capture_output=True,text=True);print(r.stdout)
json.dump(sorted(base),open('cur.json','w'))
"
```

```bash
cd /tmp && python3 ev.py 3 3
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
def ev(s):
  r=subprocess.run(['probe','evaluate','-'],input='\n'.join(s),capture_output=True,text=True);return r.stdout.strip()
for k in [1,2,3,20]:
  x=[x for x in d if d[x]==k][0]; print(k,ev([x]))
"
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
def ev(s):
  r=subprocess.run(['probe','evaluate','-'],input='\n'.join(s),capture_output=True,text=True);return r.stdout.strip()
s='b8926eb97b'
n1=[x for x in d if d[x]==1]; far=[x for x in d if d[x]==20]
print(ev([s,far[0]]))
print(ev([far[0],far[1]]))
print(ev([n1[1]]))
print(ev([s,n1[0]]))
"
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
def ev(s):
  r=subprocess.run(['probe','evaluate','-'],input='\n'.join(s),capture_output=True,text=True);return r.stdout.strip()
s='b8926eb97b'
b3=[x for x in d if d[x]<=3]
print(ev([x for x in b3 if x!=s]))
far=[x for x in d if d[x]==20][:25]
print(ev(far)); print(ev(far+[s]))
"
```

```bash
cd /tmp && python3 -c "
import json
g=json.load(open('g.json'));d=g['dist'];A={k:set(v['neighbors']) for k,v in g['adj'].items()}
s='b8926eb97b'
def st(S):
  S=set(S);ie=sum(len(A[u]&S) for u in S)//2;be=sum(len(A[u]-S) for u in S);return len(S),ie,be
for k in range(5): print('ball',k,st([x for x in d if d[x]<=k]))
far=[x for x in d if d[x]==20][:25];print('far',st(far))
print('b3-s',st([x for x in d if d[x]<=3 and x!=s]))
"
```

```bash
cd /tmp && python3 -c "
import json
g=json.load(open('g.json'));d=g['dist'];A={k:set(v['neighbors']) for k,v in g['adj'].items()}
B=set(x for x in d if d[x]<=3)
res='''313c79969e 0.9038
d3a9dc37bd 0.901
29da69359d 0.9013
6008b49c74 0.899
4cb0aae75d 0.9081
a2a357bf60 0.9107
eef2682f1e 0.9
f0fa30bcfb 0.9
a0671dafec 0.9024
d0fae90990 0.9061
0f600791ba 0.9024
3a2865f97c 0.9024
5e3fd872fc 0.9024
e6e1084a19 0.9024
4e9c76f251 0.9041
543d7b8ed2 0.9041
491b1446f4 0.9161
7a7b0c5b39 0.8998
9f24f98ecf 0.9041
c0506ceeab 0.9019
2e88892a87 0.8973
7ef4e009b3 0.8961
0653ca7955 0.8997
29ba3357fb 0.8974
734d5f2a
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
def ev(s):
  r=subprocess.run(['probe','evaluate','-'],input='\n'.join(s),capture_output=True,text=True);return r.stdout.strip()
far=[x for x in d if d[x]>=20]
for n in [5,60,200]: print(n,ev(far[:n]))
"
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
def ev(s):
  r=subprocess.run(['probe','evaluate','-'],input='\n'.join(s),capture_output=True,text=True);return r.stdout.strip()
far=[x for x in d if d[x]>=20]
print(ev(far[:199]+['b8926eb97b']))
print(ev(far[200:400]))
print(ev(far[:100]))
"
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
def ev(s):
  r=subprocess.run(['probe','evaluate','-'],input='\n'.join(s),capture_output=True,text=True);return r.stdout.strip()
far=[x for x in d if d[x]>=20]
print(3,ev(far[:3]));print(4,ev(far[:4]));print('5b',ev(far[300:305]))
"
```

```bash
cd /tmp && cat > cand.py <<'EOF'
import json,subprocess,collections,sys
g=json.load(open("g.json"));d=g["dist"];A={k:set(v['neighbors']) for k,v in g['adj'].items()}
s="b8926eb97b"
def ev(S):
    r=subprocess.run(["probe","evaluate","-"],input="\n".join(S),capture_output=True,text=True);return r.stdout.strip()
def comp(nodes):
    nodes=set(nodes)
    if s not in nodes: return set()
    seen={s};q=[s]
    while q:
        u=q.pop()
        for v in A[u]&nodes:
            if v not in seen: seen.add(v);q.append(v)
    return seen
C={}
for k in range(5,9): C[f"ball{k}"]=[x for x in d if d[x]<=k]
```

```bash
cd /tmp && cat >> cand.py <<'EOF'
for n in sys.argv[1:]: print(n,len(C[n]),ev(C[n]))
EOF
python3 cand.py ball5 ball6 ball7 ball8 sph2 sph3 deg4comp | tail -7
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist'];A={k:v['neighbors'] for k,v in g['adj'].items()}
def ev(s):
  r=subprocess.run(['probe','evaluate','-'],input='\n'.join(s),capture_output=True,text=True);return r.stdout.strip()
for k in [2,3,4,5]:
  S=[x for x in A if len(A[x])==k and d[x]>=10][:100]; print(k,len(S),ev(S))
"
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist'];A={k:v['neighbors'] for k,v in g['adj'].items()}
def ev(s):
  r=subprocess.run(['probe','evaluate','-'],input='\n'.join(s),capture_output=True,text=True);return r.stdout.strip()
for k in [1,2,3,5,6]:
  S=[x for x in A if len(A[x])==k and d[x]>=10][:1]; print(k,S,ev(S))
"
```

```bash
cd /tmp && pip list 2>/dev/null | grep -i networkx; python3 -c "
import json,networkx as nx
g=json.load(open('g.json'));G=nx.Graph()
for u,v in g['adj'].items():
  for w in v['neighbors']: G.add_edge(u,w)
s='b8926eb97b'
print(G.number_of_nodes(),G.number_of_edges(),nx.transitivity(G))
br=list(nx.bridges(G));print('bridges',len(br))
H=G.copy();H.remove_edges_from(br);c=nx.node_connected_component(H,s);print('2ecc',len(c))
for b in nx.biconnected_components(G):
  if s in b: print('bicomp',len(b))
cl=nx.clustering(G);print('clust start',cl[s],[cl[x] for x in G[s]])
print('tri start',nx.triangles(
```

```bash
cd /tmp && cat > data.py <<'EOF'
import json
g=json.load(open("g.json"));d=g["dist"];A={k:set(v['neighbors']) for k,v in g['adj'].items()}
s="b8926eb97b"
D=[]
ball=lambda k:[x for x in d if d[x]<=k]
for k,v in zip(range(5),[0.0148,0.4066,0.833,0.9024,0.8952]): D.append((ball(k),v))
for k,v in zip(range(5,9),[0.9339,0.9096,0.9249,0.9329]): D.append((ball(k),v))
B=set(ball(3))
for l in open("tog.txt"):
    x,v=l.split(); D.append((list(B^{x}),float(v)))
n1=[x for x in d if d[x]==1]; far20=[x for x in d if d[x]==20]; far=[x for x in d if d[x]>=20]
D.append(([s,far20[0]],0.3042)); D.append(([s,n1[
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/data.py').read())
import subprocess
def ev(S):
  r=subprocess.run(['probe','evaluate','-'],input='\n'.join(S),capture_output=True,text=True);return r.stdout.strip()
print(ev(far20[:3])); print(ev(far20[3:6])); print(ev([s]+far20[:2]))
print([len(A[x]) for x in far20[:6]], [len(A[x]) for x in far[:5]])
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/data.py').read())
def ie(S):
  S=set(S);return sum(len(A[u]&S) for u in S)//2
print(ie(far20[:2]),ie(far20[:3]),ie(far20[3:6]),ie(far[:4]),ie(far[:5]),ie(far[300:305]),ie([s,n1[0]]))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/data.py').read())
from math import comb
def st(S):
  S=set(S);dg={u:len(A[u]&S) for u in S};e=sum(dg.values())//2
  w=sum(comb(k,2) for k in dg.values());t=sum(1 for u in S for v in A[u]&S for x in A[v]&S if u<v<x and x in A[u])
  vol=sum(len(A[u]) for u in S); return dict(n=len(S),e=e,w=w,t=t,cut=vol-2*e,vol=vol,ins=s in S)
for S,v in D[46:]: print(v,st(S))
"
```

```bash
cd /tmp && cat > wl.py <<'EOF'
exec(open('/tmp/data.py').read())
from collections import Counter
import math
def wl(S,h):
    S=set(S);lab={u:('S' if u==s else 'P') for u in S};c=Counter(lab.values())
    for i in range(h):
        lab={u:(lab[u],tuple(sorted(lab[v] for v in A[u]&S))) for u in S}
        lab={u:str(hash(l)) for u,l in lab.items()}
        c.update(lab.values())
    return c
def cos(a,b):
    return sum(a[k]*b[k] for k in a)/math.sqrt(sum(v*v for v in a.values())*sum(v*v for v in b.values()))
def fit(T,h):
    wt=wl(T,h);err=[abs(cos(wl(S,h),wt)-v) for S,v in D]
    return max(
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/wl.py').read())
for k,h in [(4,4),(3,3)]:
  wt=wl(ball(k),h)
  print([ (round(cos(wl(S,h),wt),4),v) for S,v in D[:9]+D[46:]])
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/wl.py').read())
def kcore(S,k):
  S=set(S)
  while True:
    r={u for u in S if len(A[u]&S)<k}
    if not r: return S
    S-=r
for r in range(2,7):
  for k in [2,3]:
    C=kcore(ball(r),k); print(r,k,len(C),s in C,[round(fit(C,h)[1],4) for h in [2,3,4]])
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/wl.py').read())
def kcore(S,k):
  S=set(S)
  while True:
    r={u for u in S if len(A[u]&S)<k}
    if not r: return S
    S-=r
for r in range(2,7):
  for k in [2,3]:
    C=kcore(ball(r),k)
    if s in C: print(r,k,len(C),[round(fit(C,h)[1],4) for h in [2,3,4]])
"
```

```bash
cd /tmp && cat > srch.py <<'EOF'
exec(open('/tmp/wl.py').read())
import itertools
h=3
W=[(wl(S,h),v) for S,v in D]
def err(T):
    wt=wl(T,h);return max(abs(cos(a,wt)-v) for a,v in W)
B3=ball(3);d4=[x for x in d if d[x]==4]
res=[]
for c in itertools.combinations(d4,3):
    res.append((err(B3+list(c)),c))
res.sort();print(res[:5])
print(err(B3))
EOF
python3 srch.py
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/data.py').read())
B=set(ball(3))
for l in open('/tmp/tog.txt'):
  x,v=l.split()
  if d[x]==4:
    nb=A[x]&B; print(x,v,[(y,len(A[y]&B)) for y in nb])
"
```

```bash
cd /tmp && cat > sa.py <<'EOF'
exec(open('/tmp/wl.py').read())
import random,sys
h=int(sys.argv[1]);random.seed(int(sys.argv[2]))
W=[(wl(S,h),v) for S,v in D]
def err(T):
    wt=wl(T,h);return sum((cos(a,wt)-v)**2 for a,v in W)
pool=set(ball(6))
T=set(ball(3));
for x in [x for x in d if d[x]==4][:3]: T.add(x)
e=err(T);best=(e,set(T));temp=0.01
for it in range(6000):
    T2=set(T)
    out=random.choice([x for x in T2 if x!=s]); T2.remove(out)
    fr=[y for x in T2 for y in A[x] if y not in T2 and y in pool]
    T2.add(random.choice(fr))
    e2=err(T2)
    if e2<e or random.random()<math.exp((e-
```

```bash
cd /tmp && sed -i 's/range(6000)/range(int(sys.argv[3]))/' sa.py && for i in 2 3 4 5 6 7; do (python3 sa.py 3 $i 20000 > sb_$i.txt &) ; done; sleep 300; cat sb_*.txt | cut -c1-30
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/wl.py').read())
import ast
l=open('/tmp/sb_2.txt').read();T=ast.literal_eval(l[l.index('['):])
wt=wl(T,3)
for i,(S,v) in enumerate(D):
  p=cos(wl(S,3),wt)
  if abs(p-v)>0.003: print(i,len(S),v,round(p,4))
"
```

```bash
cd /tmp && cat > wl2.py <<'EOF'
exec(open('/tmp/data.py').read())
from collections import Counter
import math,sys
MODE=sys.argv[1]
def wl(S,h):
    S=set(S);lab={u:('S' if u==s else 'P') for u in S};its=[Counter(lab.values())]
    for i in range(h):
        lab={u:str(hash((lab[u],tuple(sorted(lab[v] for v in A[u]&S))))) for u in S}
        its.append(Counter(lab.values()))
    return its
def c1(a,b):
    na=sum(v*v for v in a.values());nb=sum(v*v for v in b.values())
    return sum(a[k]*b[k] for k in a)/math.sqrt(na*nb)
def cos(A_,B_):
    if MODE=='mean': return sum(c1(a,b) for a,b in zip(A_
```

```bash
cd /tmp && cat > sa3.py <<'EOF'
import sys,random,ast
exec(open('/tmp/wl2.py').read())
h=3;random.seed(int(sys.argv[2]))
W=[(wl(S,h),v) for S,v in D]
def err(T):
    wt=wl(T,h);return sum((cos(a,wt)-v)**2 for a,v in W)
pool=set(A)
l=open(sys.argv[3]).read();T=set(ast.literal_eval(l[l.index('['):]))
e=err(T);best=(e,set(T));temp=float(sys.argv[4])
for it in range(int(sys.argv[5])):
    T2=set(T)
    for _ in range(random.choice([1,1,2])):
        out=random.choice([x for x in T2 if x!=s]); T2.remove(out)
        fr=[y for x in T2 for y in A[x] if y not in T2]
        T2.add(random.choice(fr))
 
```

```bash
cd /tmp && python3 -c "
import sys;sys.argv=['x','sum']
exec(open('/tmp/wl2.py').read())
import ast
l=open('/tmp/sc_6.txt').read();T=ast.literal_eval(l[l.index('['):])
wt=wl(T,3)
for i,(S,v) in enumerate(D):
  p=cos(wl(S,3),wt); print(i,len(S),v,round(p,4),round(p-v,4))
" | head -50
```

```bash
cd /tmp && cat > rules.py <<'EOF'
import sys;sys.argv=['x','sum']
exec(open('/tmp/wl2.py').read())
import networkx as nx
G=nx.Graph([(u,v) for u in A for v in A[u]])
W=[(wl(S,3),v) for S,v in D]
def err(T):
    wt=wl(T,3);return sum((cos(a,wt)-v)**2 for a,v in W)
C={}
for c in list(A[s])+[x for x in d if d[x]==2]:
    dc=nx.single_source_shortest_path_length(G,c,cutoff=6)
    for r in range(1,6):
        C[f'ballaround {c} {r}']=[x for x in dc if dc[x]<=r]
for r in range(2,7):
  for k in range(2,7):
    C[f'ball{r} deg>={k}']=[x for x in d if d[x]<=r and len(A[x])>=k]
    C[f'ball{r} deg<={k}'
```

```bash
cd /tmp && python3 -c "
import ast,subprocess,json
for f in ['sc_6.txt','sc_2.txt']:
  l=open(f).read();T=ast.literal_eval(l[l.index('['):])
  r=subprocess.run(['probe','evaluate','-'],input='\n'.join(T),capture_output=True,text=True);print(f,r.stdout)
  open('/tmp/extra.txt','a').write(json.dumps([T,json.loads(r.stdout)['score']])+'\n')
"
```

```bash
cd /tmp && cat >> data.py <<'EOF'
import os
if os.path.exists('/tmp/extra.txt'):
    for l in open('/tmp/extra.txt'):
        S,v=json.loads(l); D.append((S,v))
EOF
cat > sa4.py <<'EOF'
import sys,random,ast
exec(open('/tmp/wl2.py').read())
h=3;seed=int(sys.argv[2]);random.seed(seed)
W=[(wl(S,h),v) for S,v in D]
def err(T):
    wt=wl(T,h);return sum((cos(a,wt)-v)**2 for a,v in W)
T={s}
while len(T)<29:
    T.add(random.choice([y for x in T for y in A[x] if y not in T]))
e=err(T);best=(e,set(T));temp=0.02
N=int(sys.argv[3])
for it in range(N):
    T2=set(T)
    for _ in range(random.choice([1,1
```

```bash
cd /tmp && for i in $(seq 100 179); do (python3 sa4.py sum $i 40000 > se_$i.txt &) ; done; sleep 590; ls se_*.txt | wc -l; cat se_*.txt | cut -c1-25 | sort -n | head
```

```bash
sleep 240; cd /tmp; cat se_*.txt | cut -c1-25 | sort -n | head; cat se_*.txt | wc -l
```

```bash
cd /tmp; until [ $(cat se_*.txt | wc -l) -ge 80 ]; do sleep 10; done; cat se_*.txt | cut -c1-25 | sort -n | head
```

```bash
cd /tmp; cat se_*.txt | wc -l; ps aux | grep -c sa4.py
```

```bash
cd /tmp; until [ $(cat se_*.txt | wc -l) -ge 80 ]; do sleep 10; done; cat se_*.txt | cut -c1-25 | sort -n | head
```

```bash
cat /tmp/claude-0/-app/ddb91620-4eba-47e0-9845-7c1c0704445b/tasks/b74g672l0.output; cd /tmp; cat se_*.txt | wc -l
```

```bash
cd /tmp; until [ $(cat se_*.txt | wc -l) -ge 80 ] || [ $(pgrep -fc sa4.py) -eq 0 ]; do sleep 10; done; echo "done lines=$(cat se_*.txt | wc -l)"; cat se_*.txt | cut -c1-25 | sort -n | head -5
```

**agent:** The 80 search runs are still going. I'll pick up as soon as the monitor reports they've finished.

