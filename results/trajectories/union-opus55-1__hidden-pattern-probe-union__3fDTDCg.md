# union-opus55-1 / hidden-pattern-probe-union__3fDTDCg

model=bedrock/us.anthropic.claude-opus-5-5 reward=0.0 exception=None evaluate=144 best=0.9559

```bash
probe --help; probe status
```

**agent:** Let me BFS the graph (neighbors is free).

```bash
cd /tmp && cat > bfs.py <<'EOF'
import json,subprocess,collections
s="5c37187f6d"
adj={};dist={s:0};q=collections.deque([s])
while q:
    u=q.popleft()
    out=json.loads(subprocess.check_output(["probe","neighbors",u]))
    adj[u]=out
    for v in (out if isinstance(out,list) else out.get("neighbors",[])):
        if v not in dist: dist[v]=dist[u]+1;q.append(v)
json.dump({"adj":adj,"dist":dist},open("g.json","w"))
print(len(dist),collections.Counter(dist.values()))
EOF
probe neighbors 5c37187f6d; python3 bfs.py
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
for k in [0,1,2,3,4]:
    sel=[x for x in d if d[x]<=k]
    print(k,len(sel),subprocess.check_output(['probe','evaluate']+sel).decode())
"
```

```bash
cd /tmp && python3 -c "
import json,collections
g=json.load(open('g.json'));a={k:v['neighbors'] for k,v in g['adj'].items()};d=g['dist']
asym=sum(1 for u in a for v in a[u] if u not in a[v]);print('asym',asym)
print(collections.Counter(len(v) for v in a.values()))
for k in range(5):
  print(k,[(x,len(a[x])) for x in d if d[x]==k])
"
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
base=[x for x in d if d[x]<=3]
ev=lambda s: json.loads(subprocess.check_output(['probe','evaluate']+s))['score']
for x in d:
  if d[x]==4: print('add',x,ev(base+[x]))
for x in base: print('rm',x,d[x],ev([y for y in base if y!=x]))
"
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
ev=lambda s: json.loads(subprocess.check_output(['probe','evaluate']+s))['score']
S=lambda lo,hi:[x for x in d if lo<=d[x]<=hi]
for lo,hi in [(0,5),(2,3),(2,4),(1,3),(3,3),(3,4)]:
  print(lo,hi,ev(S(lo,hi)))
"
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
ev=lambda s: json.loads(subprocess.check_output(['probe','evaluate']+s))['score']
S=lambda lo,hi:[x for x in d if lo<=d[x]<=hi]
print(ev(S(2,3)),ev(S(2,3)),ev(S(2,3)+['5c37187f6d']))
"
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
ev=lambda s: json.loads(subprocess.check_output(['probe','evaluate']+s))['score']
base=[x for x in d if 2<=d[x]<=3]+['5c37187f6d']
for x in d:
  if d[x] in(1,4): print(d[x],x,ev(base+[x]))
"
```

```bash
cd /tmp && for x in 4e85239fbf 0b09234e84 e80ad63be6; do probe evaluate $x; done; probe evaluate 5c37187f6d 4e85239fbf
```

```bash
cd /tmp && probe evaluate 4e85239fbf 1486027e39; probe evaluate 4e85239fbf 0b09234e84; python3 -c "
import json;g=json.load(open('g.json'));print([k for k,v in g['dist'].items() if v==30][:3])"; probe neighbors 4e85239fbf
```

```bash
cd /tmp && probe evaluate dfea12a08d; probe evaluate dfea12a08d 3b92ede081 fc6313d257 4e85239fbf
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
ev=lambda s: json.loads(subprocess.check_output(['probe','evaluate']+s))['score']
far=[x for x in d if d[x]>=30]
for n in [3,8,20,60]: print(n,ev(far[:n]))
"
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
ev=lambda s: json.loads(subprocess.check_output(['probe','evaluate']+s))['score']
for k in [2,4,5,6]: print('shell',k,ev([x for x in d if d[x]==k]))
for k in [6,7]: print('ball',k,ev([x for x in d if d[x]<=k]))
"
```

```bash
cd /tmp && python3 -c "
import json,subprocess
g=json.load(open('g.json'));d=g['dist']
ev=lambda s: json.loads(subprocess.check_output(['probe','evaluate']+s))['score']
xs=['1486027e39','544f3d78bd']+[x for x in d if d[x]==3][:5]+['3b92ede081','fc6313d257']
for x in xs: print(d[x],x,ev([x]))
"
```

```bash
cd /tmp && python3 -c "
import json,subprocess,random
g=json.load(open('g.json'));d=g['dist']
ev=lambda s: json.loads(subprocess.check_output(['probe','evaluate']+s))['score']
far=[x for x in d if d[x]>=30]
print(ev(['4e85239fbf','4e85239fbf']))
for n in [40,100,200]: print(n,ev(far[:n]))
random.seed(1);print('rand60',ev(random.sample(far,60)))
"
```

```bash
cd /tmp && cat > cand.py <<'EOF'
import json,collections
g=json.load(open('g.json'));a={k:v['neighbors'] for k,v in g['adj'].items()};d=g['dist'];s='5c37187f6d'
def comp(ok):
    seen={s};q=[s]
    while q:
        u=q.pop()
        for v in a[u]:
            if v not in seen and ok(v): seen.add(v);q.append(v)
    return seen
def core(k):
    alive=set(a);ch=True
    while ch:
        ch=False
        for u in list(alive):
            if sum(v in alive for v in a[u])<k: alive.discard(u);ch=True
    return alive
C={}
deg={u:len(a[u]) for u in a}
C['deg3comp']=comp(lambda v:deg[v]==3)
C['deg<=3c
```

```bash
cd /tmp && cat > ev.py <<'EOF'
import json,subprocess,collections
g=json.load(open('/tmp/g.json'));a={k:v['neighbors'] for k,v in g['adj'].items()}
def dist(c):
    D={c:0};q=collections.deque([c])
    while q:
        u=q.popleft()
        for v in a[u]:
            if v not in D: D[v]=D[u]+1;q.append(v)
    return D
ev=lambda s: json.loads(subprocess.check_output(['probe','evaluate']+list(s)))['score']
EOF
python3 -c "
import sys;sys.path.insert(0,'/tmp');from ev import *
D=dist('3b92ede081')
for lo,hi in [(0,5),(2,3),(0,3)]: print(lo,hi,ev([x for x in D if lo<=D[x]<=hi]))
"
```

```bash
cd /tmp && probe evaluate 5c37187f6d dfea12a08d; probe evaluate 5c37187f6d 1486027e39 4e85239fbf; probe evaluate 1486027e39 4e85239fbf 544f3d78bd
```

```bash
cd /tmp && python3 -c "
import sys;sys.path.insert(0,'/tmp');from ev import *
d=g['dist']
base=[x for x in d if 2<=d[x]<=3]+['5c37187f6d','e80ad63be6','e594085ae5']
b=ev(base);print('base',b)
for x in base[:-3]:
  print('rm',d[x],x,ev([y for y in base if y!=x]))
"
```

```bash
cd /tmp && python3 -c "
import sys;sys.path.insert(0,'/tmp');from ev import *
d=g['dist']
base=[x for x in d if 2<=d[x]<=3]+['5c37187f6d','e80ad63be6','e594085ae5']
for add in [['cd50b387e3'],['f8c57d620e'],['cd50b387e3','f8c57d620e'],['9a5f3d20a4'],['ea72afe57f'],['d22616f016'],['4e85239fbf']]:
  print(add,ev(base+add))
"
```

```bash
cd /tmp && python3 -c "
import sys;sys.path.insert(0,'/tmp');from ev import *
d=g['dist']
base=[x for x in d if d[x]<=3 and x not in('1486027e39','544f3d78bd')]+['e80ad63be6','e594085ae5']
print(ev(base+['1486027e39']),ev(base+['544f3d78bd']),ev(base+['1486027e39','544f3d78bd']))
for x in ['e80ad63be6','e594085ae5']: print(x,[(y,d[y]) for y in a[x]])
"
```

```bash
cd /tmp && python3 -c "
import sys;sys.path.insert(0,'/tmp');from ev import *
d=g['dist']
for x in sorted([x for x in d if d[x]<=4],key=lambda x:d[x]):
  c=[sum(d[y]==d[x]+k for y in a[x]) for k in(-1,0,1)]
  print(d[x],x,len(a[x]),c)
"
```

```bash
cd /tmp && python3 -c "
import sys;sys.path.insert(0,'/tmp');from ev import *
d=g['dist'];s='5c37187f6d'
best=set([x for x in d if 2<=d[x]<=3]+[s,'e80ad63be6','e594085ae5','4e85239fbf'])
for alpha in [0.1,0.15,0.3,0.5]:
  p={u:0 for u in a};p[s]=1;r=dict(p)
  for it in range(200):
    n={u:0 for u in a}
    for u in a:
      for v in a[u]: n[v]+=r[u]/len(a[u])
    r={u:alpha*(u==s)+(1-alpha)*n[u] for u in a}
  rk=sorted(a,key=lambda u:-r[u])
  top=set(rk[:19]);print(alpha,len(top&best),[(x[:4],d[x]) for x in rk[:25] if x not in best])
"
```

```bash
cd /tmp && python3 -c "
import sys;sys.path.insert(0,'/tmp');from ev import *
d=g['dist'];s='5c37187f6d'
best=[x for x in d if 2<=d[x]<=3]+[s,'e80ad63be6','e594085ae5','4e85239fbf']
for x in ['26ed6d5137','013152936d','6f3564ba95','71e8cf11ba','0cb6510ee9','eee53bc995','18ac937242','c182366d47']:
  print(x,ev(best+[x]))
"
```

```bash
probe status
```

```bash
cd /tmp && python3 -c "
import sys;sys.path.insert(0,'/tmp');from ev import *
d=g['dist'];s='5c37187f6d'
best=[x for x in d if 2<=d[x]<=3]+[s,'e80ad63be6','e594085ae5','4e85239fbf']
for x in ['6930b3ece9','f39000d409','d90ecca08a']:
  print(x,ev([y for y in best if y!=x]))
"
```

```bash
cd /tmp && python3 -c "
import sys;sys.path.insert(0,'/tmp');from ev import *
d=g['dist'];s='5c37187f6d'
best=[x for x in d if 2<=d[x]<=3 and x!='6930b3ece9']+[s,'e80ad63be6','e594085ae5','4e85239fbf']
for x in ['57229fd2af','f39000d409','4d4e4cc142']:
  print(x,ev([y for y in best if y!=x]))
"
```

**agent:** The best set I found scores 0.9559, not 1.0, so this submission almost certainly won't count as a match. I'm submitting it because not submitting also scores zero.

```bash
cd /tmp && python3 -c "
import json
g=json.load(open('/tmp/g.json'));d=g['dist']
best=[x for x in d if 2<=d[x]<=3 and x!='6930b3ece9']+['5c37187f6d','e80ad63be6','e594085ae5','4e85239fbf']
print('\n'.join(best))" | probe submit -
```

**agent:** I submitted an 18-item selection that scored 0.9559 under `evaluate`. That is short of 1.0, and any submission that doesn't match scores zero, so this one most likely fails. I never worked out the rule that defines the target.

**What I found:**
- **The system:** about 1,600 items, all reachable from the start item, each linked to between 1 and 7 others.
- **The score isn't overlap with the target.** Any single item other than the start scored 0.4064, wherever it was. The start alone, which is in the target, scored only 0.0102. A connected block of 100 items about 30 links away from the start scored 0.952, as high as anything near the start.
- **No simple rule I tried reached 1.0:**
  - all items within *r* links of the start (*r* = 0–7): best 0.886
  - items exactly *r* links away: best 0.944, for distances 2–3 together
  - degree-based connected components and k-cores
  - top-*N* by personalized PageRank from the start (checked offline; it didn't match my best set)
- **Hill-climbing** with the rest of the budget stalled at about 0.956.

**What I submitted:** the start item, all items 2–3 links away except `6930b3ece9`, one direct neighbour (`4e85239fbf`), and two items 4 links away (`e80ad63be6`, `e594085ae5`). Each of those two links back to two items at distance 3.

I used 144 of the 150 evaluate calls. Most went on trying to decode the scoring function; spending them on candidate rules instead might have found the target.

