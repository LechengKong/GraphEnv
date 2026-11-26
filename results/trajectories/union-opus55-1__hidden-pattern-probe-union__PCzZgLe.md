# union-opus55-1 / hidden-pattern-probe-union__PCzZgLe

model=bedrock/us.anthropic.claude-opus-5-5 reward=0.0 exception=AgentTimeoutError evaluate=107 best=0.9758

```bash
probe --help; probe status
```

**agent:** Let me explore the graph with BFS (neighbors is free).

```bash
mkdir -p /tmp/w && cd /tmp/w && probe neighbors 5c37187f6d; cat > bfs.py <<'EOF'
import json,subprocess,collections
s="5c37187f6d"
adj={};dist={s:0};q=collections.deque([s])
while q:
    u=q.popleft()
    if dist[u]>=6: continue
    r=json.loads(subprocess.check_output(["probe","neighbors",u]))
    adj[u]=r
    for v in (r if isinstance(r,list) else r.get("neighbors",[])):
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
json.dump({"adj":adj,"dist":dist},open("g.json","w"))
print(collections.Counter(dist.values()))
EOF
python3 bfs.py
```

```bash
cd /tmp/w && sed -i 's/>=6/>=100/' bfs.py && python3 bfs.py && python3 -c "
import json;g=json.load(open('g.json'));a=g['adj'];d=g['dist']
deg={u:len(v['neighbors']) for u,v in a.items()}
import collections;print(collections.Counter(deg.values()))
# directed?
asym=sum(1 for u in a for v in a[u]['neighbors'] if u not in a[v]['neighbors']);print('asym',asym)
for k in range(4):print(k,[(u,deg[u]) for u in d if d[u]==k])
"
```

```bash
cd /tmp/w && for k in 0 1 2 3 4; do python3 -c "
import json;d=json.load(open('g.json'))['dist']
print('\n'.join(u for u in d if d[u]<=$k))" | probe evaluate -; echo; done
```

```bash
cd /tmp/w && cat > ev.py <<'EOF'
import json,subprocess,sys
def ev(items):
    r=subprocess.run(["probe","evaluate","-"],input="\n".join(items),capture_output=True,text=True)
    return json.loads(r.stdout)["score"]
EOF
python3 -c "
import json;from ev import ev
d=json.load(open('g.json'))['dist']
b3=[u for u in d if d[u]<=3]
for u in [u for u in d if d[u]==4]: print('add',u,ev(b3+[u]))
for u in b3[1:]: print('rm',u,d[u],ev([x for x in b3 if x!=u]))
"
```

```bash
cd /tmp/w && python3 -c "
import json;g=json.load(open('g.json'));a={u:v['neighbors'] for u,v in g['adj'].items()};d=g['dist']
for u in d:
  if d[u]<=4: print(d[u],u,len(a[u]),[(v,d[v]) for v in a[u]])
"
```

```bash
cd /tmp/w && python3 -c "
from ev import ev
s='5c37187f6d'
for x in ['1486027e39','4e85239fbf','544f3d78bd']: print(x,ev([s,x]))
print('nostart',ev(['1486027e39','4e85239fbf','544f3d78bd']))
"
```

**agent:** Interesting: removing the start item *raised* the score, so this isn't a plain overlap metric. Testing whether the score depends on which items are chosen or only on the shape of the selection.

```bash
cd /tmp/w && python3 -c "
import json;from ev import ev
g=json.load(open('g.json'));d=g['dist']
far=[u for u in d if d[u]>=15][:19]
print('far19',ev(far))
print('far2',ev(far[:2]))
print('far1',ev(far[:1]))
"
```

```bash
cd /tmp/w && python3 -c "
import json;from ev import ev
g=json.load(open('g.json'));d=g['dist'];a={u:v['neighbors'] for u,v in g['adj'].items()}
far=[u for u in d if d[u]>=15]
bydeg={}
for u in far: bydeg.setdefault(len(a[u]),u)
for k in sorted(bydeg): print(k,ev([bydeg[k]]))
print('dup start',ev(['5c37187f6d','1486027e39']), ev(['1486027e39']), ev(['544f3d78bd','1486027e39']))
"
```

```bash
cd /tmp/w && python3 -c "
import json;from ev import ev
g=json.load(open('g.json'));d=g['dist']
far=[u for u in d if d[u]>=15]
for n in [4,6,9,30,60,120,200]: print(n,ev(far[:n]))
"
```

```bash
cd /tmp/w && python3 -c "
import json;from ev import ev
g=json.load(open('g.json'));d=g['dist']
far=[u for u in d if d[u]>=15]
print(ev(far[:9]),ev(far[:9][::-1]))
import random;random.seed(1);r=random.sample(far,9);print('rand9',ev(r))
"
```

```bash
cd /tmp/w && python3 -c "
import json;from ev import ev
g=json.load(open('g.json'));d=g['dist'];a={u:v['neighbors'] for u,v in g['adj'].items()}
far=[u for u in d if d[u]>=15]
s='5c37187f6d'
print('s+far9',ev([s]+far[:9]))
f9=far[:9];print('edges far9',sum(1 for u in f9 for v in a[u] if v in f9)//2, [d[u] for u in f9])
b2=[u for u in d if d[u]<=2];print('edges b2',sum(1 for u in b2 for v in a[u] if v in b2)//2)
b2n=b2[1:];print('b2 minus s',ev(b2n))
"
```

```bash
cd /tmp/w && python3 -c "
import json;from ev import ev
g=json.load(open('g.json'));d=g['dist']
for k in [2,3,5,8]:
  u=[x for x in d if d[x]==k][0]; print(k,ev([u]))
f15=[u for u in d if d[u]==15]; f20=[u for u in d if d[u]==20]
import random;random.seed(2)
print('rand15x9',ev(random.sample(f15,9)),len(f15))
"
```

```bash
probe status
```

```bash
cd /tmp/w && python3 -c "
import json,collections;from ev import ev
g=json.load(open('g.json'));d=g['dist']
c=collections.Counter(d.values());acc=0
for k in sorted(c): acc+=c[k]; print(k,c[k],acc)
" | head -12
```

```bash
cd /tmp/w && python3 -c "
import json;from ev import ev
g=json.load(open('g.json'));d=g['dist']
for k in range(5,11): print(k,ev([u for u in d if d[u]<=k]))
"
```

```bash
cd /tmp/w && cat > cand.py <<'EOF'
import json,collections
g=json.load(open('g.json'));d=g['dist'];a={u:v['neighbors'] for u,v in g['adj'].items()}
s='5c37187f6d';deg={u:len(a[u]) for u in a}
def comp(pred):
    seen={s};q=[s]
    while q:
        u=q.pop()
        for v in a[u]:
            if v not in seen and pred(v): seen.add(v);q.append(v)
    return seen
C={}
for k in range(2,8):
    C[f'deg<={k}']=comp(lambda v:deg[v]<=k)
    C[f'deg>={k}']=comp(lambda v:deg[v]>=k)
C['deg==3']=comp(lambda v:deg[v]==3)
# k-core
def core(k):
    alive=set(a);ch=True
    while ch:
        ch=False
        
```

```bash
cd /tmp/w && python3 -c "
import json;from ev import ev
g=json.load(open('g.json'));d=g['dist'];a={u:v['neighbors'] for u,v in g['adj'].items()}
far=[u for u in d if d[u]>=15]
for c in far:
  if len(a[c])==3 and not any(w in a[x] for x in a[c] for w in a[c]): break
print('farstar',ev([c]+a[c]))
print('star1486',ev(['1486027e39']+a['1486027e39']))
"
```

```bash
cd /tmp/w && python3 -c "
import json,collections;g=json.load(open('g.json'));d=g['dist']
c=collections.Counter(d.values());print(sorted(c.items()))"
```

```bash
cd /tmp/w && cat > model.py <<'EOF'
import json,collections,math,random
g=json.load(open('g.json'));d=g['dist'];a={u:set(v['neighbors']) for u,v in g['adj'].items()}
s='5c37187f6d'
far=[u for u in d if d[u]>=15]
ball=lambda k:[u for u in d if d[u]<=k]
b3=ball(3)
obs=[]
for k,sc in zip(range(11),[0.0102,0.392,0.6509,0.8758,0.8673,0.8682,0.8857,0.8815,0.8747,0.8696,0.8693]): obs.append((ball(k),sc))
obs+= [([s,'1486027e39'],0.2945),(['1486027e39','4e85239fbf','544f3d78bd'],0.4064),(far[:19],0.7666),(far[:2],0.4064),(far[:4],0.514),(far[:6],0.5959),(far[:9],0.6843),(far[:30],0.7203),(far[:60],0.7
```

```bash
cd /tmp/w && python3 -c "
from model import *
import collections
def bfs(src,A=a):
    D={src:0};q=[src]
    for u in q:
        for v in A[u]:
            if v not in D: D[v]=D[u]+1;q.append(v)
    return D
# balls around nearby nodes
for u in ball(2):
    D=bfs(u);print(u,d[u],[sum(1 for x in D if D[x]<=r) for r in range(1,7)])
# 2-hop graph etc
"
```

```bash
cd /tmp/w && cat > c2.py <<'EOF'
from model import *
def bfs(src,S=None):
    D={src:0};q=[src]
    for u in q:
        for v in a[u]:
            if v not in D and (S is None or v in S): D[v]=D[u]+1;q.append(v)
    return D
C={}
D5=bfs('544f3d78bd');C['ball5@544f']=[x for x in D5 if D5[x]<=5]
deg={u:len(a[u]) for u in a}
for k in range(4,9):
    B=ball(k)
    for m in range(2,7):
        for op in ['<=','>=']:
            S=[u for u in B if (deg[u]<=m if op=='<=' else deg[u]>=m) or u==s]
            # connected comp from s
            Dc=bfs(s,set(S));S=list(Dc)
            if 35<=len(S)<=48:
```

```bash
cd /tmp/w && python3 -c "
from model import *
order=sorted(d,key=lambda u:(d[u],u));T=order[:41]
for h in [4,5,6,8]:
  fT=wl(T,h,lambda u:u==s)
  r=[(round(cos(wl(S,h,lambda u:u==s),fT),3),sc) for S,sc in obs]
  print(h,round(sum((x-y)**2 for x,y in r),4),r[:12])
"
```

```bash
cd /tmp/w && cat > sa.py <<'EOF'
from model import *
import sys,random
h=int(sys.argv[1]);random.seed(int(sys.argv[2]))
L=lambda u:u==s
obsF=[(wl(S,h,L),sc) for S,sc in obs]
def err(T):
    fT=wl(T,h,L);return sum((cos(f,fT)-sc)**2 for f,sc in obsF)
def connected(T):
    D={s};q=[s]
    for u in q:
        for v in a[u]:
            if v in T and v not in D: D.add(v);q.append(v)
    return len(D)==len(T)
order=sorted(d,key=lambda u:(d[u],u));T=set(order[:41]);e=err(T);best=(e,set(T))
temp=0.01
for it in range(6000):
    T2=set(T);r=random.random()
    bd=[v for u in T2 for v in a[u] if v not i
```

```bash
cd /tmp/w && echo "02dc311858 0cb6510ee9 0e081da7d3 1486027e39 169474169a 17e635dd03 1ff2900e69 261825bee2 26b8b4d69b 2c70288ed9 2e58878c8a 39892ee110 4850869563 4889381fbd 5c37187f6d 5e2e3f6f40 6930b3ece9 6aaf1439c3 712b44bec6 7260c32d18 76bbd4a4be 7c0f8e8d28 81a680afe7 8cd96495c8 8d749effa2 9515f90da5 952b204a1a ac20b06380 b2f083b976 b3dffeb9fd bc21bbdab1 cd1ffa5781 ce8e6eec7f d40c358165 d770274437 e92e0a8616 eadcccf262 f0506666e4 f0efbb7df2 f1b43c7d6f f39000d409 f579526e04 fc638a0234" | tr ' ' '\n' > sa3.txt; probe evaluate - < sa3.txt
```

**agent:** 0.9717, so the model is close. I'll iterate: add each new measurement to the data, refit, and evaluate the new best set.

```bash
cd /tmp/w && python3 - <<'EOF'
import re
src=open('sa.py').read()
src=src.replace("obsF=[(wl(S,h,L),sc) for S,sc in obs]","""import os
extra=json.load(open('extra.json')) if os.path.exists('extra.json') else []
obs=obs+[(S,sc) for S,sc in extra]
obsF=[(wl(S,h,L),sc) for S,sc in obs]""")
src=src.replace("T=set(order[:41])","T=set(open(sys.argv[3]).read().split()) if len(sys.argv)>3 else set(order[:41])")
src=src.replace("print(' '.join(sorted(best[1])))","open(f'best{h}_{sys.argv[2]}.txt','w').write('\\n'.join(sorted(best[1])))")
open('sa2.py','w').write(src)
EOF
python3 -c "
import json;json.d
```

```bash
cd /tmp/w && sed -i 's/if r<0.4 or len(T2)<38/if r<0.5 or len(T2)<41/; s/if r>=0.4 or len(T2)>44/if len(T2)>41/' sa2.py && grep -n "T2" sa2.py | head; cat > loop.sh <<'EOF'
cd /tmp/w
init=${1:-sa3.txt}
for round in 1 2 3 4 5 6; do
  for i in 1 2 3; do python3 sa2.py 3 $((round*10+i)) $init > /dev/null & done; wait
  b=$(for i in 1 2 3; do f=best3_$((round*10+i)).txt; echo "$(python3 -c "
import sys;sys.argv=['x','3','0'];exec(open('sa2.py').read().split('order=')[0]);print(err(set(open('$f').read().split())))") $f"; done | sort -n | head -1 | awk '{print $2}')
  sc=$(probe evaluate - < $b | py
```

```bash
cd /tmp/w && python3 -c "
from c2 import bfs
from model import *
D=bfs('544f3d78bd');print('\n'.join(x for x in D if D[x]<=5))" 2>/dev/null | grep -v '^[0-9.]* ' > b544.txt; wc -l b544.txt; probe evaluate - < b544.txt
```

```bash
cd /tmp/w && python3 -c "
from model import *
import json,collections
e=json.load(open('extra.json'))
from c2 import bfs
for S,sc in e:
  S=set(S);E=sum(1 for u in S for v in a[u] if v in S)//2
  ideg=collections.Counter(sum(v in S for v in a[u]) for u in S)
  D=bfs(s,S)
  print(sc,len(S),E,sorted(ideg.items()),'startdeg',sum(v in S for v in a[s]),'ecc',max(D.values()),collections.Counter(D.values()))
" 2>&1 | grep -v '^[0-9.]* [a-z]'
```

```bash
cd /tmp/w && python3 -c "
import sys;sys.argv=['x','3','0']
exec(open('sa2.py').read().split('order=')[0])
C={}
for lo in range(1,15):
  for hi in range(lo,16):
    T=[s]+[u for u in d if lo<=d[u]<=hi]
    if 30<=len(T)<=55: C[(lo,hi)]=T
r=sorted((err(set(T)),k,len(T)) for k,T in C.items());print(r[:8])
"
```

```bash
cd /tmp/w && sed 's/    if not connected(T2): continue/    pass/' sa2.py > sa3.py && sed -i "s/best{h}_/free{h}_/" sa3.py && for h in 2 3 4; do for i in 1 2; do python3 sa3.py $h $i best3_63.txt & done; done; wait
```

```bash
cd /tmp/w && python3 -c "
import sys;sys.argv=['x','3','0']
exec(open('sa2.py').read().split('order=')[0])
T=set(open('free3_1.txt').read().split());fT=wl(T,3,L)
for S,sc in obs: 
  p=cos(wl(S,3,L),fT)
  if abs(p-sc)>0.003: print(round(p,4),sc,len(S))
print(len(obs))
"
```

```bash
cd /tmp/w && cat > sav.py <<'EOF'
from model import *
import sys,random,os
h=int(sys.argv[1]);var=sys.argv[2];random.seed(int(sys.argv[3]))
extra=json.load(open('extra.json'));obs=obs+[(S,sc) for S,sc in extra]
def feats(S):
    S=set(S);lab={u:(u==s) for u in S};its=[collections.Counter(lab.values())]
    for i in range(h):
        if 'set' in var: lab={u:(lab[u],tuple(sorted(set(lab[v] for v in a[u] if v in S)))) for u in S}
        else: lab={u:(lab[u],tuple(sorted(lab[v] for v in a[u] if v in S))) for u in S}
        its.append(collections.Counter(lab.values()))
    return its
def sim(F,G)
```

```bash
cd /tmp/w && python3 -c "
from model import *
from c2 import bfs
def prof(S):
  S=set(S);E=sum(1 for u in S for v in a[u] if v in S)//2
  return len(S),E,sorted(collections.Counter(sum(v in S for v in a[u]) for u in S).items()),sum(v in S for v in a[s])
for k in range(3,7): print('ball',k,prof(ball(k)))
" 2>&1 | grep -v '^[0-9.]* [a-z0-9]'
```

```bash
cd /tmp/w && pip list 2>/dev/null | grep -i networkx; python3 -c "
from model import *
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]])
def prof(S):
  S=set(S);H=G.subgraph(S);return len(S),H.number_of_edges(),sorted(collections.Counter(dict(H.degree()).values()).items()),H.degree(s) if s in S else None
for k in range(3,9):
  H=nx.k_core(G.subgraph(ball(k)),2)
  if s in H: print('core2ball',k,prof(H.nodes()))
for comp in nx.biconnected_components(G):
  if s in comp: print('bicon',prof(comp))
" 2>&1 | grep -v '^[0-9.]* [a-z0-9]'
```

**agent:** The 2-core of the radius-5 ball has exactly 41 nodes, although its edge count (62) is higher than the fit suggests. Checking its model error, then evaluating it:

```bash
cd /tmp/w && python3 -c "
import sys;sys.argv=['x','3','0']
exec(open('sa2.py').read().split('order=')[0])
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]])
T=set(nx.k_core(G.subgraph(ball(5)),2).nodes());print(err(T),err(set(open('free3_1.txt').read().split())))
open('c2b5.txt','w').write('\n'.join(T))
"; probe evaluate - < c2b5.txt
```

**agent:** Not a match (0.9264). Next I'll enumerate connected components containing the start inside degree-filtered subgraphs, for every set of allowed degrees.

```bash
cd /tmp/w && python3 -c "
import sys;sys.argv=['x','3','0']
exec(open('sa2.py').read().split('order=')[0])
import itertools,networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]]);deg=dict(G.degree())
res=[]
for r in range(1,7):
  for ds in itertools.combinations([1,2,4,5,6,7],r):
    allowed=set(ds)|{3}
    H=G.subgraph([u for u in G if deg[u] in allowed])
    c=nx.node_connected_component(H,s)
    if 20<=len(c)<=200: res.append((err(set(c)),len(c),sorted(allowed)))
for x in sorted(res)[:10]: print(x)
print(len(res))
"
```

```bash
cd /tmp/w && python3 -c "
import sys;sys.argv=['x','3','0']
exec(open('sa2.py').read().split('order=')[0])
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]])
ds=nx.single_source_shortest_path_length(G,s)
res=[]
for X in G:
  dx=nx.single_source_shortest_path_length(G,X)
  P={u for u in G if ds[u]+dx[u]==ds[X]}
  if 30<=len(P)<=55: res.append((err(P),len(P),X,ds[X]))
res.sort();print(res[:10],len(res))
"
```

**agent:** Strong lead: sets of the form "all items on shortest paths from the start to some item X" fit the data as well as the free search did (error ≈0.0008–0.001). Narrowing to size 41:

```bash
cd /tmp/w && python3 -c "
import sys;sys.argv=['x','3','0']
exec(open('sa2.py').read().split('order=')[0])
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]])
ds=nx.single_source_shortest_path_length(G,s)
res=[]
for X in G:
  dx=nx.single_source_shortest_path_length(G,X)
  P={u for u in G if ds[u]+dx[u]==ds[X]}
  if len(P)==41: res.append((round(err(P),5),X,ds[X],G.degree(X)))
res.sort();print(res[:15],len(res))
"
```

```bash
cd /tmp/w && python3 -c "
from model import a,s
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]])
ds=nx.single_source_shortest_path_length(G,s);X='e29478d14f'
dx=nx.single_source_shortest_path_length(G,X)
open('sp.txt','w').write('\n'.join(u for u in G if ds[u]+dx[u]==ds[X]))"; probe evaluate - < sp.txt
```

```bash
cd /tmp/w && python3 -c "
from model import *
import networkx as nx,random,json
random.seed(5)
G=nx.Graph([(u,v) for u in a for v in a[u]])
farN=[u for u in d if d[u]>=20]
seen={};qs=[]
def key(S):
  H=G.subgraph(S);return nx.weisfeiler_lehman_graph_hash(H,iterations=3)
for size in [2,3,3,4,4,4,5,5,5,6,6]:
  for t in range(200):
    S={random.choice(farN)}
    while len(S)<size:
      S.add(random.choice([v for u in S for v in a[u] if v not in S]))
    k=key(S)
    if k not in seen: seen[k]=1;qs.append(sorted(S));break
# start-containing small structures
nb=sorted(a[s]);qs.append([s]+nb[:2]);q
```

```bash
cd /tmp/w && python3 -c "
import json;from ev import ev
qs=json.load(open('qs.json'));e=json.load(open('extra.json'))
for S in qs:
  sc=ev(S);print(len(S),sc);e.append([S,sc])
for f,sc in [('c2b5.txt',0.9264),('sp.txt',0.9679),('b544.txt',0.8747)]: e.append([open(f).read().split(),sc])
json.dump(e,open('extra.json','w'))
"
```

```bash
cd /tmp/w && (for i in 1 2 3; do timeout 110 python3 sav.py 3 multi $i free3_1.txt & done; timeout 110 python3 sav.py 3 multi 4 sp.txt & wait) 2>&1 | grep multi
```

```bash
cd /tmp/w && python3 -c "
import sys;sys.argv=['x','3','multi','0','free3_1.txt']
exec(open('sav.py').read().split('T=set(')[0])
T=set(open('v_3_multi_2.txt').read().split());fT=feats(T)
import json
for S,sc in json.load(open('extra.json'))[-16:]: print(len(S),round(sim(feats(S),fT),4),sc)
F=fT;print([dict(x) for x in F[:2]])
"
```

```bash
cd /tmp/w && python3 -c "
from model import *
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]])
for k in range(2,16):
  R=[u for u in d if d[u]==k];H=G.subgraph(R)
  print(k,len(R),H.number_of_edges(),sorted(collections.Counter(dict(H.degree()).values()).items()))
"
```

```bash
cd /tmp/w && python3 -c "
import sys;sys.argv=['x','3','multi','0','free3_1.txt']
exec(open('sav.py').read().split('T=set(')[0])
for f in ['v_3_multi_2.txt','v_3_multi_1.txt','free3_1.txt']:
  T=set(open(f).read().split());fT=feats(T)
  print(f,err(T),[round(sim(feats(S),fT),4) for S,sc in obs if s in S][:8])
print([sc for S,sc in obs if s in S][:8])
"
```

```bash
cd /tmp/w && python3 -c "
import sys;sys.argv=['x','3','multi','0','free3_1.txt']
exec(open('sav.py').read().split('T=set(')[0])
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]])
ds=nx.single_source_shortest_path_length(G,s)
res=[]
for X in G:
  dx=nx.single_source_shortest_path_length(G,X)
  P={u for u in G if ds[u]+dx[u]==ds[X]}
  if 30<=len(P)<=55: res.append((round(err(P),5),len(P),X,ds[X]))
res.sort();print(res[:10])
print(err(set(open('v_3_multi_1.txt').read().split())))
"
```

```bash
cd /tmp/w && python3 -c "
from model import *
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]])
for f in ['v_3_multi_1.txt','v_3_multi_3.txt','free3_1.txt']:
  T=open(f).read().split();H=G.subgraph(T)
  print(f,len(T),H.number_of_edges(),nx.number_connected_components(H),sorted(collections.Counter(dict(H.degree()).values()).items()),'start',H.degree(s),[H.degree(v) for v in H[s]], 'cycles',len(nx.cycle_basis(H)), 'girths',sorted(len(c) for c in nx.minimum_cycle_basis(H)))
"
```

```bash
cd /tmp/w && python3 -c "
from model import *
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]])
tr=nx.triangles(G)
c=collections.Counter(d[u] for u in G if tr[u]>0);print(sorted(c.items())[:20])
print('total tri',sum(tr.values())//3)
"
```

```bash
nproc; cd /tmp/w && sed -e 's/range(5000)/range(int(sys.argv[5]))/' -e 's/temp\*=0.999/temp*=float(sys.argv[6])/' -e "s/T2.add(random.choice(bd))/T2.add(random.choice(bd) if random.random()<0.8 else random.choice(pool))/" -e "s/^T=set(open(sys.argv\[4\]).read().split())/pool=[u for u in d if 1<=d[u]<=40]\nT=set(open(sys.argv[4]).read().split())/" -e "s/open(f'v_/open(f'w_/" sav.py > sav2.py && grep -n "pool\|argv" sav2.py
```

**agent:** The machine has 192 cores, so I'll run 48 parallel annealing restarts on all the data and then evaluate the best candidates.

```bash
cd /tmp/w && for i in $(seq 100 147); do f=$([ $((i%3)) = 0 ] && echo v_3_multi_1.txt || ([ $((i%3)) = 1 ] && echo sp.txt || echo free3_1.txt)); timeout 580 python3 sav2.py 3 multi $i $f 15000 0.9996 > log_$i.txt & done; wait; cat log_1*.txt | sort -k3 -g | head
```

```bash
cd /tmp/w && cat > run.sh <<'EOF'
cd /tmp/w
fs=(v_3_multi_1.txt sp.txt free3_1.txt)
for i in $(seq 100 147); do
  f=${fs[$((i % 3))]}
  timeout 580 python3 sav2.py 3 multi $i $f 15000 0.9996 > log_$i.txt &
done
wait
cat log_1*.txt | sort -k3 -g | head
EOF
bash run.sh
```

```bash
cd /tmp/w && cat log_1*.txt | sort -k3 -g | head; ls w_* | wc -l
```

**agent:** Every run hit the time limit before writing output. I'll lower the iteration count and have each run save its best set periodically.

```bash
cd /tmp/w && python3 - <<'EOF'
s=open('sav2.py').read()
s=s.replace("    temp*=float(sys.argv[6])","    temp*=float(sys.argv[6])\n    if it%500==0: open(f'w_{h}_{var}_{sys.argv[3]}.txt','w').write('\\n'.join(sorted(best[1])));open(f'log_{sys.argv[3]}.txt','w').write(f'{h} {var} {best[0]}\\n')")
open('sav2.py','w').write(s)
EOF
sed -i 's/15000 0.9996/8000 0.9993/' run.sh; timeout 590 bash run.sh
```

```bash
cd /tmp/w && for f in log_1*.txt; do echo "$(cat $f) $f"; done | sort -k3 -g | head -3; 
```

```bash
cd /tmp/w && cat > evadd.py <<'EOF'
import json,sys;from ev import ev
e=json.load(open('extra.json'))
for f in sys.argv[1:]:
    S=open(f).read().split();sc=ev(S);print(f,len(S),sc);e.append([S,sc])
json.dump(e,open('extra.json','w'))
EOF
python3 evadd.py w_3_multi_146.txt w_3_multi_116.txt
```

```bash
cd /tmp/w && python3 -c "
from model import *
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]])
for f in ['w_3_multi_146.txt','w_3_multi_116.txt']:
  T=open(f).read().split();H=G.subgraph(T)
  print(f,len(T),H.number_of_edges(),[len(c) for c in nx.connected_components(H)],sorted(collections.Counter(dict(H.degree()).values()).items()),'start',H.degree(s),[H.degree(v) for v in H[s]], 'tri',sum(nx.triangles(H).values())//3)
  print(sorted(d[u] for u in T))
"; probe status
```

```bash
cd /tmp/w && cat > rules.py <<'EOF'
import sys;sys.argv=['x','3','multi','0','free3_1.txt']
exec(open('sav.py').read().split('T=set(')[0])
import networkx as nx,itertools
G=nx.Graph([(u,v) for u in a for v in a[u]])
C={}
tr=nx.triangles(G);deg=dict(G.degree())
for r in range(2,12):
    B=ball(r)
    C[f'tri_ball{r}']=[u for u in B if tr[u]>0 or u==s]
    H=G.subgraph(B)
    for k in [2,3]:
        K=nx.k_core(H,k)
        C[f'core{k}ball{r}']=list(K.nodes())+([s] if s not in K else [])
    C[f'2ec_ball{r}']=[c for c in nx.k_edge_components(H,2) if s in c][0]
    for dd in range(2,7):
        C
```

```bash
cd /tmp/w && cat >> rules.py <<'EOF'
print('---')
ds=nx.single_source_shortest_path_length(G,s)
far=[u for u in G if ds[u]==max(ds.values())]
U=set()
for X in far:
    dx=nx.single_source_shortest_path_length(G,X);P={u for u in G if ds[u]+dx[u]==ds[X]};U|=P
    print(X,len(P),err(P))
print('union',len(U),err(U))
EOF
python3 rules.py | sed -n '/---/,$p'
```

```bash
cd /tmp/w && cat > rules2.py <<'EOF'
exec(open('rules.py').read().split("res=sorted")[0])
small=[(feats(S),sc) for S,sc in obs if len(S)<=10]
def errs(T):
    fT=feats(T);return sum((sim(f,fT)-sc)**2 for f,sc in small)
ds=nx.single_source_shortest_path_length(G,s)
for X in G:
    if ds[X]<=12:
        dx=nx.single_source_shortest_path_length(G,X);C['sp'+X]={u for u in G if ds[u]+dx[u]==ds[X]}
for f in ['w_3_multi_146.txt','v_3_multi_1.txt']: C[f]=set(open(f).read().split())
res=sorted((errs(set(T)),n,len(T)) for n,T in C.items() if 15<=len(T)<=70)
for x in res[:15]: print(x)
print(len(small))

```

```bash
cd /tmp/w && cat > chk.py <<'EOF'
exec(open('rules.py').read().split("res=sorted")[0])
T=set(open(sys.argv[1] if len(sys.argv)>1 else 'w_3_multi_146.txt').read().split())
import sys as _s
T=set(open(_s.argv[-1]).read().split()) if False else T
EOF
python3 - <<'EOF'
import sys;sys.argv=['x']
exec(open('/tmp/w/rules.py').read().split("res=sorted")[0].replace("sys.argv=['x','3','multi','0','free3_1.txt']","sys.argv=['x','3','multi','0','/tmp/w/free3_1.txt']"))
EOF
echo
```

```bash
cd /tmp/w && cat > chk.py <<'EOF'
import sys;arg=sys.argv[1:]
sys.argv=['x','3','multi','0','free3_1.txt']
exec(open('sav.py').read().split('T=set(')[0])
T=set(open(arg[0]).read().split());fT=feats(T)
print('norm',math.sqrt(sum(sum(v*v for v in c.values()) for c in fT)))
for S,sc in obs:
    if s in S and len(S)<=10: print(len(S),round(sim(feats(S),fT),4),sc)
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]]);H=G.subgraph(T);print('startdeg',H.degree(s))
print(fT[1])
EOF
python3 chk.py w_3_multi_146.txt
```

```bash
cd /tmp/w && sed -e "s/T2.discard(random.choice(\[u for u in T2 if u!=s\]))/T2.discard(random.choice([u for u in T2 if u not in keep]))/" -e "s/^pool=/keep={s}|a[s]\npool=/" -e "s/open(f'w_/open(f'k_/g" -e "s/open(f'log_/open(f'klog_/" sav2.py > sav3.py && python3 -c "
from model import *
open('init_k.txt','w').write('\n'.join(ball(4)[:41]))" && cat > runk.sh <<'EOF'
cd /tmp/w
for i in $(seq 200 231); do timeout 400 python3 sav3.py 3 multi $i init_k.txt 6000 0.9992 > /dev/null & done; wait
for f in klog_*.txt; do echo "$(cat $f) $f"; done | sort -k3 -g | head -3
EOF
timeout 450 bash runk.sh
```

```bash
cd /tmp/w && python3 chk.py k_3_multi_210.txt; python3 -c "
from model import *
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]])
T=open('k_3_multi_210.txt').read().split();H=G.subgraph(T)
print(len(T),H.number_of_edges(),sorted(collections.Counter(dict(H.degree()).values()).items()),[(v,H.degree(v)) for v in H[s]])
print(sorted(d[u] for u in T))"
```

```bash
cd /tmp/w && cat > cyc.py <<'EOF'
import sys;sys.argv=['x','3','multi','0','free3_1.txt']
exec(open('sav.py').read().split('T=set(')[0])
def cycles_through(L):
    U={};
    # DFS simple paths from s, length<=L, closing at s
    best={}
    stack=[(s,[s])]
    res=set()
    def dfs(u,path,vis):
        for v in a[u]:
            if v==s and len(path)>=3: 
                for x in path: res.add(x)
                for x in path: best[x]=min(best.get(x,99),len(path))
            elif v not in vis and len(path)<L:
                vis.add(v);path.append(v);dfs(v,path,vis);path.pop();vis.discard(v)

```

**agent:** Cycle unions don't fit. I'll redo the constrained search properly: exactly 41 items, containing the start and all three of its neighbors, using clean swap moves.

```bash
cd /tmp/w && cat > sak.py <<'EOF'
import sys;arg=sys.argv[1:]
sys.argv=['x','3','multi','0','free3_1.txt']
exec(open('sav.py').read().split('T=set(')[0])
random.seed(int(arg[0]));keep={s}|a[s]
pool=[u for u in d if 1<=d[u]<=int(arg[2])]
T=set(open(arg[1]).read().split());e=err(T);best=(e,set(T));temp=0.005
for it in range(int(arg[3])):
    T2=set(T)
    bd=list({v for u in T2 for v in a[u] if v not in T2})
    add=random.choice(bd) if random.random()<0.85 else random.choice([p for p in pool if p not in T2])
    T2.add(add);T2.discard(random.choice([u for u in T2 if u not in keep and u!=add]))

```

```bash
cd /tmp/w && for f in q_320.txt q_339.txt q_316.txt; do python3 -c "
from model import *
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]])
T=open('$f').read().split();H=G.subgraph(T)
print('$f',len(T),H.number_of_edges(),[len(c) for c in nx.connected_components(H)],sorted(collections.Counter(dict(H.degree()).values()).items()),[(v[:4],H.degree(v)) for v in H[s]],'tri',sum(nx.triangles(H).values())//3)
print(sorted(d[u] for u in T))"; done
```

```bash
cd /tmp/w && cat > var.py <<'EOF'
import sys;sys.argv=['x','3','multi','0','free3_1.txt']
exec(open('sav.py').read().split('T=set(')[0])
import networkx as nx
G=nx.Graph([(u,v) for u in a for v in a[u]])
def prof(T):
    H=G.subgraph(T);return (len(T),H.number_of_edges(),sorted(collections.Counter(dict(H.degree()).values()).items()))
C={}
G2=nx.k_core(G,2)
for r in range(3,9):
    B=ball(r);H=G.subgraph(B)
    C[f'b{r}-leaves1']=[u for u in B if H.degree(u)>=2]
    C[f'b{r}-leaves2']=[u for u in C[f'b{r}-leaves1'] if G.subgraph(C[f'b{r}-leaves1']).degree(u)>=2]
    C[f'b{r}-Gdeg1']=[u for u in
```

```bash
cd /tmp/w && cat >> var.py <<'EOF'
print('----')
deg=dict(G.degree())
for k in range(3,8):
  for lo in [1,2,3]:
    Gk=G.subgraph([u for u in G if lo<=deg[u]<=k or u==s])
    dd=nx.single_source_shortest_path_length(Gk,s)
    for r in range(3,15):
        B=[u for u in dd if dd[u]<=r]
        for nm,T in [('ball',B),('core',[*nx.k_core(Gk.subgraph(B),2)])]:
            if 33<=len(T)<=50: print(k,lo,r,nm,prof(T),round(err(set(T)),4))
EOF
python3 var.py | sed -n '/----/,$p' | sort -k8 -g | head
```

**agent:** Degree-capped balls don't fit either. I'll check which items near the start the best constrained fits agree on, to see the target's actual shape.

```bash
cd /tmp/w && python3 -c "
from model import *
import glob,collections
fs=[]
for f in glob.glob('qlog_*.txt'):
  e=float(open(f).read().split()[0]);fs.append((e,f.replace('qlog','q')))
fs.sort();top=fs[:15];print([round(x[0],5) for x in top])
c=collections.Counter(u for e,f in top for u in open(f).read().split())
for k in range(0,8):
  print(k,[(u[:4],c[u]) for u in d if d[u]==k])
"
```

```bash
cd /tmp/w && python3 -c "
from model import *
import json
far=[u for u in d if d[u]>=15]
out={}
for k in [4,5]:
  for c in far:
    if len(a[c])>=k:
      nb=sorted(a[c])
      import itertools
      for comb in itertools.combinations(nb,k):
        if not any(y in a[x] for x in comb for y in comb): out[k]=[c]+list(comb);break
      if k in out: break
json.dump(out,open('stars.json','w'));print({k:len(v) for k,v in out.items()})
"; python3 -c "
import json;from ev import ev
st=json.load(open('stars.json'));e=json.load(open('extra.json'))
for k,S in st.items(): sc=ev(S);print(k,sc);e.append([S,
```

```bash
cd /tmp/w && cat > sah.py <<'EOF'
import sys;arg=sys.argv[1:]
sys.argv=['x','3','multi','0','free3_1.txt']
exec(open('sav.py').read().split('T=set(')[0])
random.seed(int(arg[0]));keep=set(ball(2))
want={2:20,3:16,4:5}
def pen(T):
    c=collections.Counter(sum(v in T for v in a[u]) for u in T)
    return sum(abs(c.get(k,0)-want.get(k,0)) for k in set(c)|set(want))
def tot(T): return err(T)+0.002*pen(T)
pool=[u for u in d if 1<=d[u]<=int(arg[2])]
T=set(open(arg[1]).read().split())|keep
while len(T)>41: T.discard(random.choice([u for u in T if u not in keep]))
e=tot(T);best=(e,set(T));temp=0.005

```

