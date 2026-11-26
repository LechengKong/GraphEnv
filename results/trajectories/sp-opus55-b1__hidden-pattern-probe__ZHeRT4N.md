# sp-opus55-b1 / hidden-pattern-probe__ZHeRT4N

model=bedrock/us.anthropic.claude-opus-5-5 reward=0.0 exception=AgentTimeoutError evaluate=95 best=0.9408

```bash
probe --help; probe status
```

**agent:** Let me BFS the graph fully (neighbors is free).

```bash
cd /tmp && cat > bfs.py <<'EOF'
import json,subprocess,collections
s="b8926eb97b"
adj={};dist={s:0};q=collections.deque([s])
while q:
    u=q.popleft()
    out=json.loads(subprocess.check_output(["probe","neighbors",u]))
    nb=out if isinstance(out,list) else out.get("neighbors",out)
    adj[u]=nb
    for v in nb:
        if v not in dist: dist[v]=dist[u]+1;q.append(v)
    if len(adj)>3000: break
json.dump({"adj":adj,"dist":dist},open("g.json","w"))
print(len(adj),len(dist),collections.Counter(dist.values()))
EOF
probe neighbors b8926eb97b; python3 bfs.py
```

```bash
cd /tmp && cat > ev.py <<'EOF'
import json,subprocess,sys
g=json.load(open("g.json"));d=g["dist"]
for r in map(int,sys.argv[1:]):
    sel=[k for k,v in d.items() if v<=r]
    out=subprocess.run(["probe","evaluate","-"],input="\n".join(sel),capture_output=True,text=True).stdout
    print(r,len(sel),out)
EOF
python3 ev.py 0 1 2 3 5 8
```

```bash
cd /tmp && python3 ev.py 4 6 7 9
```

```bash
cd /tmp && cat > ev2.py <<'EOF'
import json,subprocess,sys
def ev(sel):
    out=subprocess.run(["probe","evaluate","-"],input="\n".join(sel),capture_output=True,text=True).stdout
    return json.loads(out)["score"]
EOF
cat > t.py <<'EOF'
import json;from ev2 import ev
g=json.load(open("g.json"));d=g["dist"];adj=g["adj"]
base=[k for k,v in d.items() if v<=2]
for k in base:
    print("rm",k,d[k],len(adj[k]),ev([x for x in base if x!=k]))
EOF
python3 t.py
```

```bash
cd /tmp && python3 -c "
import json;from ev2 import ev
g=json.load(open('g.json'));d=g['dist']
b=[k for k,v in d.items() if v<=2]
print(ev(b),ev(b))"
```

```bash
cd /tmp && python3 -c "
import json,collections
g=json.load(open('g.json'));adj=g['adj'];d=g['dist']
print(sum(len(v) for v in adj.values())/2, collections.Counter(len(v) for v in adj.values()))
s='b8926eb97b'
for k,v in d.items():
  if v<=2: print(k,v,[(x,d[x]) for x in adj[k]])
"
```

```bash
cd /tmp && python3 -c "
import json;from ev2 import ev
g=json.load(open('g.json'));d=g['dist']
s='b8926eb97b'
b=[k for k,v in d.items() if v<=9]
print(ev([x for x in b if x!=s]))
print(ev([s,'40234ca2ac']), ev(['40234ca2ac']), ev(['02ac8fd827']))
"
```

```bash
cd /tmp && python3 -c "
import json;from ev2 import ev
g=json.load(open('g.json'));d=g['dist']
for r in [1,3,5,10,20,45]:
  k=[x for x,v in d.items() if v==r][0]; print(r,ev([k]))
"
```

```bash
cd /tmp && python3 -c "
import json;from ev2 import ev
g=json.load(open('g.json'));d=g['dist'];adj=g['adj']
far=[x for x,v in d.items() if v==30]
a=far[0]; b=adj[a][0]
print(ev([a,b]), ev([a,far[1]]), ev([a,far[1],far[2]]), ev(far[:10]))
"
```

```bash
cd /tmp && python3 -c "
import json;from ev2 import ev
g=json.load(open('g.json'));d=g['dist'];adj=g['adj']
s='b8926eb97b'
far=[x for x,v in d.items() if v>=30]
for k in [1,3,10,50]: print(k,ev([s]+far[:k]), ev(far[:k]))
"
```

```bash
cd /tmp && python3 -c "
import json;from ev2 import ev
g=json.load(open('g.json'));d=g['dist'];adj=g['adj']
s='b8926eb97b'
for deg in [1,2,3,4,5,6,7]:
  ks=[x for x in adj if len(adj[x])==deg and x!=s][:1]
  print(deg,[ (d[k],ev([k])) for k in ks])
print([len(adj[x]) for x in [x for x,v in d.items() if v in(1,3,5,10,20,45)]][:10])
"
```

```bash
cd /tmp && python3 -c "
import json
g=json.load(open('g.json'));adj=g['adj']
print(sum(1 for u in adj for v in adj[u] if u not in adj[v]))
"
cat > ev3.py <<'EOF'
import json,subprocess,sys
g=json.load(open("g.json"));d=g["dist"]
for r in map(int,sys.argv[1:]):
    sel=[k for k,v in d.items() if v==r]+(['b8926eb97b'] if r else [])
    out=subprocess.run(["probe","evaluate","-"],input="\n".join(sel),capture_output=True,text=True).stdout
    print(r,len(sel),out.strip())
EOF
python3 ev3.py 1 2 3
```

```bash
cd /tmp && cat > lib.py <<'EOF'
import json,subprocess,collections
g=json.load(open("g.json"));adj=g["adj"];D=g["dist"];S='b8926eb97b'
def ev(sel):
    out=subprocess.run(["probe","evaluate","-"],input="\n".join(sel),capture_output=True,text=True).stdout
    return json.loads(out)["score"]
def ball(c,r):
    d={c:0};q=collections.deque([c])
    while q:
        u=q.popleft()
        if d[u]==r: continue
        for v in adj[u]:
            if v not in d: d[v]=d[u]+1;q.append(v)
    return list(d)
EOF
python3 -c "
from lib import *
c=[x for x,v in D.items() if v==30][0]
b=ball(c,2); print(len(b
```

```bash
cd /tmp && python3 -c "
import networkx as nx
from lib import *
G=nx.Graph([(u,v) for u in adj for v in adj[u]])
core=nx.core_number(G); print('core start',core[S], collections.Counter(core.values()))
from networkx.algorithms import community as c
for res in [0.5,1,2]:
  cs=c.louvain_communities(G,resolution=res,seed=1)
  m=[x for x in cs if S in x][0]; print(res,len(cs),len(m))
print(nx.transitivity(G), nx.diameter(G))
"
```

```bash
cd /tmp && python3 -c "
import networkx as nx
from lib import *
G=nx.Graph([(u,v) for u in adj for v in adj[u]])
K=nx.k_core(G,3)
cc=nx.node_connected_component(K,S); print(len(cc))
if len(cc)<=200: print(ev(list(cc)))
from networkx.algorithms import community as c
cs=c.louvain_communities(G,resolution=1,seed=1)
m=[x for x in cs if S in x][0]; print(len(m),ev(list(m)))
"
```

```bash
cd /tmp && python3 -c "
from lib import *
for r in [10,20,40,46]:
  c=[x for x,v in D.items() if v==r][0]
  b=ball(c,2); print(r,len(b),ev(b))
"
```

```bash
cd /tmp && python3 -c "
from lib import *
x='40234ca2ac'
print(ev([x,S]),ev([S,x]))
"
```

```bash
cd /tmp && cat > cands.py <<'EOF'
import networkx as nx, pickle
from lib import *
G=nx.Graph([(u,v) for u in adj for v in adj[u]])
C={}
deg=dict(G.degree())
for k in [2,3]:
    K=nx.k_core(G,k); 
    if S in K: C[f'core{k}']=nx.node_connected_component(K,S)
# reachable via nodes with degree filter
for op,name in [(lambda d:d>=4,'deg>=4'),(lambda d:d<=4,'deg<=4'),(lambda d:d==4,'deg==4'),(lambda d:d>=3,'deg>=3'),(lambda d:d>=5,'deg>=5'),(lambda d:d<=3,'deg<=3')]:
    H=G.subgraph([n for n in G if op(deg[n]) or n==S]); C[name]=nx.node_connected_component(H,S)
from networkx.algorithms import comm
```

```bash
cd /tmp && python3 -c "
import networkx as nx
from lib import *
from networkx.algorithms import community as c
G=nx.Graph([(u,v) for u in adj for v in adj[u]])
cs=c.louvain_communities(G,resolution=1,seed=1)
print(c.modularity(G,cs), sorted(len(x) for x in cs))
"
```

```bash
cd /tmp && python3 -c "
import pickle
from lib import *
C=pickle.load(open('C.pkl','rb'))
for k in ['deg==4','deg>=5','deg<=3','louv0.3','louv0.5','louv0.7','louv1.5','louv2','louv3','greedy','lpa']:
  print(k,len(C[k]),ev(C[k]))
"
```

```bash
probe status
```

```bash
cd /tmp && python3 -c "
from lib import *
for r in [20,40]:
  c=[x for x,v in D.items() if v==r][0]
  for rad in range(5,15):
    b=ball(c,rad)
    if len(b)>=150: break
  b=b[:174] if len(b)>174 else b
  print(r,rad,len(b),ev(b))
"
```

```bash
cd /tmp && python3 -c "
from lib import *
import random
random.seed(5)
nodes=[x for x in adj if x!=S]
for i in range(3):
  s=random.sample(nodes,10); print(ev(s), sum(1 for a in s for b in adj[a] if b in s))
"
```

```bash
cd /tmp && python3 -c "
from lib import *
far=[x for x,v in D.items() if v==30][:10]
print(sum(1 for a in far for b in adj[a] if b in far)/2)
far=[x for x,v in D.items() if v>=30][:50]
print(sum(1 for a in far for b in adj[a] if b in far)/2)
"
```

```bash
cd /tmp && python3 -c "
from lib import *
import random
random.seed(7)
nodes=[x for x in adj if x!=S]
# independent set of 100
s=[];
random.shuffle(nodes)
for x in nodes:
  if all(y not in s for y in adj[x]): s.append(x)
  if len(s)==100: break
print(ev(s[:50]),ev(s[:100]), ev(s[:100]+[S]))
"
```

```bash
cd /tmp && python3 -c "
from lib import *
far=[x for x,v in D.items() if v==30][:10]
print([sum(1 for b in adj[a] if b in far) for a in far])
c=[x for x,v in D.items() if v==30][0]; b=adj[c][0]
print(c,b,[x for x in adj[c]])
"
```

```bash
cd /tmp && python3 -c "
from lib import *
c='7c68283178'; n=adj[c]
print('wedge',ev([c,n[0],n[1]]))
print('star3',ev([c]+n[:3]))
print('path4', end=' ')
a,b=n[0],c; nxt=[x for x in adj[n[0]] if x!=c and x not in adj[c]][0]
print(ev([nxt,n[0],c,n[1]]))
"
```

```bash
cd /tmp && python3 -c "
from lib import *
import networkx as nx
G=nx.Graph([(u,v) for u in adj for v in adj[u]])
b3=[k for k,v in D.items() if v<=3]; print('r3',len(b3))
sh4=[k for k,v in D.items() if v==4]
# shell 4 nodes and how many ball-3 neighbors
for x in sh4: print(x,sum(1 for y in adj[x] if D[y]==3))
H=G.subgraph(b3); print('deg1 in r3',[ (x,D[x]) for x in b3 if H.degree(x)==1])
"
```

```bash
cd /tmp && cat > rules.py <<'EOF'
from lib import *
import networkx as nx, itertools
G=nx.Graph([(u,v) for u in adj for v in adj[u]])
out={}
for k in [2,3]:
    K=nx.k_core(G,k)
    for r in range(1,8):
        b=nx.single_source_shortest_path_length(K,S,cutoff=r); out[f'core{k}ball{r}']=set(b)
# closure: from ball r, add nodes with >=2 nbrs in set iteratively
for r in range(1,5):
    s=set(k for k,v in D.items() if v<=r)
    t=set(s); ch=True
    while ch:
        ch=False
        for x in list(G):
            if x not in t and sum(1 for y in adj[x] if y in t)>=2: t.add(x); ch=True
        if
```

```bash
cd /tmp && python3 -c "
import pickle
from lib import *
R=pickle.load(open('R.pkl','rb'))
print(R['close2_r1']==R['ball3+2nb'], sorted(D[x] for x in R['close2_r1']))
for k in ['close2_r1','multsp5']: print(k,ev(list(R[k])))
"
```

```bash
cd /tmp && python3 -c "
import pickle
from lib import *
R=pickle.load(open('R.pkl','rb'))
print('b3+2nb',ev(list(R['ball3+2nb'])))
b3=[k for k,v in D.items() if v<=3]
four=['313c79969e','4cb0aae75d','a2a357bf60','d0fae90990']
for x in four: print(x, ev(b3+[y for y in four if y!=x]))
"
```

```bash
cd /tmp && python3 -c "
from lib import *
c='7c68283178'; n=adj[c]
nxt=[x for x in adj[n[0]] if x!=c and x not in adj[c]][0]
for s in [[c,n[0],n[1]],[c]+n[:3],[nxt,n[0],c,n[1]]]:
  print([(a[:4],b[:4]) for i,a in enumerate(s) for b in s[i+1:] if b in adj[a]])
"; probe status
```

```bash
cd /tmp && cat > obs.py <<'EOF'
from lib import *
import random,pickle
O=[]
def add(s,v): O.append((list(s),v))
for r,v in zip(range(10),[0.0148,0.4066,0.833,0.9024,0.8952,0.9339,0.9096,0.9249,0.9329,0.9393]):
    add([k for k,x in D.items() if x<=r],v)
base=[k for k,v in D.items() if v<=2]
rm=[0.9041,0.8008,0.7608,0.7717,0.8051,0.8073,0.8374,0.7962,0.8317,0.766,0.7669,0.7631,0.8161]
for k,v in zip(base,rm): add([x for x in base if x!=k],v)
add([S,'40234ca2ac'],0.3042); add(['40234ca2ac'],0.4154)
for r,v in [(2,0.6011),(3,0.6729)]: add([k for k,x in D.items() if x==r]+[S],v)
for r,v in [(30,0.
```

```bash
cd /tmp && cat > fit.py <<'EOF'
import pickle,random,math,sys,collections
from lib import *
O=pickle.load(open('O.pkl','rb'))
H=int(sys.argv[1]); seed=int(sys.argv[2])
def feats(s):
    s=set(s); lab={x:('s' if x==S else 'o') for x in s}; c=collections.Counter(lab.values())
    for i in range(H):
        lab={x:(lab[x],tuple(sorted(lab[y] for y in adj[x] if y in s))) for x in s}
        c.update(lab.values())
    return c
OF=[(feats(s),v) for s,v in O]
for f,_ in OF: f['_n']=math.sqrt(sum(x*x for k,x in f.items() if k!='_n'))
def err(T):
    ft=feats(T); nt=math.sqrt(sum(x*x for x in ft.values
```

```bash
cd /tmp && for h in 3 4 5; do for s in 2 3; do python3 fit.py $h $s & done; done; wait
```

```bash
sleep 100; cat /tmp/claude-0/-app/944c4261-a9b6-4580-929a-5c7fcff14210/tasks/bcw6ldz5d.output
```

```bash
cd /tmp && cat > resid.py <<'EOF'
import pickle,math,sys,collections
from lib import *
O=pickle.load(open('O.pkl','rb'))
H=int(sys.argv[1]); T=pickle.load(open(sys.argv[2],'rb'))
def feats(s):
    s=set(s); lab={x:('s' if x==S else 'o') for x in s}; c=collections.Counter(lab.values())
    for i in range(H):
        lab={x:(lab[x],tuple(sorted(lab[y] for y in adj[x] if y in s))) for x in s}
        c.update(lab.values())
    return c
def cos(a,b): return sum(a[k]*b[k] for k in a if k in b)/math.sqrt(sum(x*x for x in a.values())*sum(x*x for x in b.values()))
ft=feats(T)
for i,(s,v) in enumerate(
```

```bash
pkill -f fit.py; cd /tmp && cat > fit2.py <<'EOF'
import pickle,random,math,sys,collections
from lib import *
O=pickle.load(open('O.pkl','rb'))
H=int(sys.argv[1]); seed=int(sys.argv[2]); MODE=sys.argv[3]; ITER=int(sys.argv[4])
def feats(s):
    s=set(s); lab={x:('s' if x==S else 'o') for x in s}; c=collections.Counter(lab.values())
    for i in range(H):
        if MODE=='ms': lab={x:(lab[x],tuple(sorted(lab[y] for y in adj[x] if y in s))) for x in s}
        elif MODE=='set': lab={x:(lab[x],tuple(sorted(set(lab[y] for y in adj[x] if y in s)))) for x in s}
        elif MODE=='noown': lab={x:(i
```

```bash
cd /tmp && for m in ms set noown deg; do for h in 2 3 4; do python3 fit2.py $h 1 $m 4000 >> fit2.out & done; done; wait; sort -k4 -g fit2.out
```

```bash
until [ $(wc -l < /tmp/fit2.out 2>/dev/null || echo 0) -ge 12 ]; do sleep 5; done; sort -k4 -g /tmp/fit2.out
```

```bash
sort -k4 -g /tmp/fit2.out
```

```bash
cat /tmp/claude-0/-app/944c4261-a9b6-4580-929a-5c7fcff14210/tasks/bef3l208l.output; ls -la /tmp/fit2.out /tmp/T_*
```

**agent:** The heredoc never ran because pkill killed that shell first. Rewriting the script and launching it again.

```bash
cd /tmp && cat > fit2.py <<'EOF'
import pickle,random,math,sys,collections
from lib import *
O=pickle.load(open('O.pkl','rb'))
H=int(sys.argv[1]); seed=int(sys.argv[2]); MODE=sys.argv[3]; ITER=int(sys.argv[4])
def feats(s):
    s=set(s); lab={x:('s' if x==S else 'o') for x in s}; c=collections.Counter(lab.values())
    for i in range(H):
        if MODE=='ms': lab={x:(lab[x],tuple(sorted(lab[y] for y in adj[x] if y in s))) for x in s}
        elif MODE=='set': lab={x:(lab[x],tuple(sorted(set(lab[y] for y in adj[x] if y in s)))) for x in s}
        elif MODE=='noown': lab={x:(i,tuple(sorted(lab
```

```bash
cd /tmp && rm -f fit2.out; for m in ms set noown deg; do for h in 2 3 4; do python3 fit2.py $h 1 $m 4000 >> fit2.out & done; done; wait; sort -k4 -g fit2.out
```

```bash
until [ $(wc -l < /tmp/fit2.out) -ge 12 ]; do sleep 5; done; sort -k4 -g /tmp/fit2.out
```

**agent:** The fits for four kernel variants (each at WL depths 2–4) are running in the background. I'll pick the variant that reproduces the recorded scores exactly when they finish.

```bash
sort -k4 -g /tmp/fit2.out
```

```bash
cd /tmp && sed -i 's/^T=set(k for k,v in D.items() if v<=3)|set(random.sample(\[k for k,v in D.items() if v==4\],3))/T=set(k for k,v in D.items() if v<=3)|set(random.sample([k for k,v in D.items() if v==4],3))\nif len(sys.argv)>5: T=pickle.load(open(sys.argv[5],"rb"))/' fit2.py && rm -f fit3.out; for h in 3 4 5 6; do for s in 11 12; do python3 fit2.py $h $s ms 15000 >> fit3.out & done; done; wait; sort -k4 -g fit3.out
```

**agent:** Eight longer fit runs (depths 3–6, two seeds each) are going in the background. I'll compare them when they finish.

