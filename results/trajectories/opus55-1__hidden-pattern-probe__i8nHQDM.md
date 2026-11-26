# opus55-1 / hidden-pattern-probe__i8nHQDM

model=bedrock/us.anthropic.claude-opus-5-5 reward=1.0 exception=None evaluate=106 best=1.0

```bash
probe --help; probe status
```

**agent:** Let me crawl the graph via BFS (neighbors is free).

```bash
mkdir -p /tmp/w && cd /tmp/w && cat > crawl.py <<'EOF'
import json,subprocess,collections
s="b8926eb97b"
adj={};dist={s:0};q=collections.deque([s])
while q:
    u=q.popleft()
    out=json.loads(subprocess.run(["probe","neighbors",u],capture_output=True,text=True).stdout)
    adj[u]=out
    if len(adj)>3000: break
    for v in (out if isinstance(out,list) else out.get("neighbors",[])):
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
json.dump({"adj":adj,"dist":dist},open("g.json","w"))
print(len(adj),len(dist),collections.Counter(dist.values()))
EOF
probe neighbors b8926eb97b; python3 
```

```bash
cd /tmp/w && python3 -c "
import json,collections
g=json.load(open('g.json'));adj={k:v['neighbors'] for k,v in g['adj'].items()};d=g['dist']
print(collections.Counter(len(v) for v in adj.values()))
print(all(u in adj[v] for u in adj for v in adj[u]))
"
for r in 0 1 2 3 4; do python3 -c "
import json;g=json.load(open('g.json'));print('\n'.join(k for k,v in g['dist'].items() if v<=$r))" | probe evaluate -; done
```

```bash
cd /tmp/w && cat > t.py <<'EOF'
import json,subprocess,sys
g=json.load(open('g.json'));d=g['dist']
base=[k for k,v in d.items() if v<=3]
def ev(sel):
    r=subprocess.run(["probe","evaluate","-"],input="\n".join(sel),capture_output=True,text=True).stdout
    return json.loads(r)["score"]
res={}
for k,v in d.items():
    if v==4: res[k]=ev(base+[k])
    elif 1<=v<=3: res[k]=ev([x for x in base if x!=k])
json.dump(res,open('res.json','w'))
adj={k:v['neighbors'] for k,v in g['adj'].items()}
for k,s in sorted(res.items(),key=lambda x:d[x[0]]): print(d[k],k,len(adj[k]),s)
EOF
python3 t.py
```

```bash
cd /tmp/w && for i in 1 2; do python3 -c "
import json;g=json.load(open('g.json'));print('\n'.join(k for k,v in g['dist'].items() if v<=3))" | probe evaluate -; done
```

```bash
cd /tmp/w && python3 -c "
import json
g=json.load(open('g.json'));adj={k:v['neighbors'] for k,v in g['adj'].items()};d=g['dist'];res=json.load(open('res.json'))
B=0.9024
def lab(k):
  s=res[k]
  if d[k]==4: return 'IN' if s>B else ('?' if s==B else 'out')
  return 'IN' if s<B else 'out'
for k in sorted(res,key=lambda k:d[k]):
  print(d[k],k,lab(k),[(n[:4],d[n],lab(n) if n in res else ('S' if d[n]==0 else '-')) for n in adj[k]])
"
```

```bash
probe evaluate b8926eb97b e6f6a117af; probe evaluate b8926eb97b 40234ca2ac; probe evaluate e6f6a117af; probe evaluate 40234ca2ac
```

**agent:** The score isn't a simple overlap measure (singletons of neighbors score higher than start+neighbor). Testing some shape hypotheses.

```bash
cd /tmp/w && for c in "v==2" "v==3" "2<=v<=3" "1<=v<=3" "2<=v<=4" "v==0 or 2<=v<=3" "1<=v<=4"; do echo "$c"; python3 -c "
import json;g=json.load(open('g.json'));print('\n'.join(k for k,v in g['dist'].items() if $c))" | probe evaluate -; done
```

```bash
cd /tmp/w && cat > lab.py <<'EOF'
import json
g=json.load(open('g.json'));d=g['dist'];res=json.load(open('res.json'))
B=0.9024
def lab(k):
  s=res[k]
  if d[k]==4: return 'IN' if s>B else ('?' if s==B else 'out')
  return 'IN' if s<B else 'out'
IN=[k for k in res if lab(k)=='IN']; Q=[k for k in res if lab(k)=='?']
json.dump({'IN':IN,'Q':Q},open('lab.json','w'))
EOF
python3 lab.py; python3 -c "
import json;l=json.load(open('/tmp/w/lab.json'));print('\n'.join(l['IN']))" | probe evaluate -;python3 -c "
import json;l=json.load(open('/tmp/w/lab.json'));print('\n'.join(l['IN']+['b8926eb97b']))" | pr
```

```bash
cd /tmp/w && probe evaluate 02ac8fd827; probe evaluate 491b1446f4; probe evaluate 40234ca2ac e6f6a117af; python3 -c "
import json;g=json.load(open('g.json'));print([k for k,v in g['dist'].items() if v==20][0])" | probe evaluate -
```

```bash
cd /tmp/w && cat > ev.py <<'EOF'
import json,subprocess,sys,collections
g=json.load(open('/tmp/w/g.json'));adj={k:v['neighbors'] for k,v in g['adj'].items()};d=g['dist']
def ball(c,r):
    D={c:0};q=collections.deque([c])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in D: D[v]=D[u]+1; q.append(v)
    return [k for k,x in D.items() if x<=r]
def ev(sel):
    r=subprocess.run(["probe","evaluate","-"],input="\n".join(sel),capture_output=True,text=True)
    return r.stdout.strip() or r.stderr
EOF
python3 -c "
import sys;sys.path.insert(0,'/tmp/w');from ev import 
```

```bash
cd /tmp/w && python3 -c "
import sys,random;sys.path.insert(0,'/tmp/w');from ev import *
random.seed(1)
far=[k for k,v in d.items() if v>=15]
for n in [26,50,100]: print(n,ev(random.sample(far,n)))
print(len(ball(far[0],3)), len(ball(far[0],1)))
"
```

```bash
cd /tmp/w && python3 -c "
import sys,random;sys.path.insert(0,'/tmp/w');from ev import *
far=[k for k,v in d.items() if v==20]
print(ev(ball(far[0],2)))
print(ev(ball(far[0],4)))
print(ev(ball(far[1],3)), len(ball(far[1],3)))
print(ev(ball('b8926eb97b',3)[:0]+ball(far[0],3)+['b8926eb97b']))
"
```

```bash
cd /tmp/w && python3 -c "
import sys;sys.path.insert(0,'/tmp/w');from ev import *
far=[k for k,v in d.items() if v==20]
s='b8926eb97b'
def st(S):
  S=set(S);m=sum(1 for u in S for v in adj[u] if v in S)//2;b=sum(1 for u in S for v in adj[u] if v not in S)
  return len(S),m,b,round(2*m/(2*m+b),3) if m+b else 0
for nm,S,sc in [('sr1',ball(s,1),.4066),('sr2',ball(s,2),.833),('sr3',ball(s,3),.9024),('sr4',ball(s,4),.8952),('fr1',ball(far[0],1),.7612),('fr2',ball(far[0],2),.8941),('fr3',ball(far[0],3),.9178),('fr4',ball(far[0],4),.9089),('f1r3',ball(far[1],3),.9174)]: print(nm,sc,st(S))
"
```

```bash
cd /tmp/w && python3 -c "
import sys;sys.path.insert(0,'/tmp/w');from ev import *
far=[k for k,v in d.items() if v==20]
x=far[0]
print(ev([x,adj[x][0]]))
print(ev(['b8926eb97b',x]))
print(ev(ball(x,1)+['b8926eb97b']))
"
```

```bash
cd /tmp/w && python3 -c "
import sys;sys.path.insert(0,'/tmp/w');from ev import *
far=[k for k,v in d.items() if v==20]
tri=path=None
for x in far:
  for y in adj[x]:
    for z in adj[y]:
      if z!=x:
        if z in adj[x] and not tri: tri=[x,y,z]
        if z not in adj[x] and not path: path=[x,y,z]
print(tri,path)
print(ev(tri));print(ev(path))
"
```

```bash
cd /tmp/w && cat > hc.py <<'EOF'
import sys,json;sys.path.insert(0,'/tmp/w');from ev import *
S=set(k for k,v in d.items() if 2<=v<=3); best=0.9241
moves=sys.argv[1].split(',')
for m in moves:
    T=S^{m}
    out=json.loads(ev(sorted(T))); s=out['score']
    print(m,d[m],'add' if m not in S else 'rem',s,out['evaluate_used'])
    if s>best: best=s;S=T
json.dump(sorted(S),open('/tmp/w/best.json','w')); print(best)
EOF
python3 hc.py 491b1446f4,a2a357bf60,4cb0aae75d,734d5f2a17,313c79969e,d0fae90990,9f24f98ecf,aaf16439e9,e7a1da5fa7
```

```bash
cd /tmp/w && sed -i 's/^S=set.*$/S=set(json.load(open("\/tmp\/w\/best.json"))); best=float(sys.argv[2])/' hc.py && python3 hc.py 4e9c76f251,543d7b8ed2,a0671dafec,0f600791ba,3a2865f97c,5e3fd872fc,e6e1084a19,29da69359d,eef2682f1e 0.9395
```

```bash
cd /tmp/w && python3 -c "
import sys,json;sys.path.insert(0,'/tmp/w');from ev import *
S=set(json.load(open('best.json')))
ids=lambda u:sum(v in S for v in adj[u])
for p in ['29ba3357fb','0a8fed595a','e7c3e13a01','4a7b0c9fbd','bc7a8654b4','7a7b0c5b39']: print(p,ids(p),len(adj[p]),d[p])
for p in ['4e9c76f251','543d7b8ed2','a0671dafec','0f600791ba','3a2865f97c','5e3fd872fc','e6e1084a19','29da69359d']: print(p,ids(p),len(adj[p]),[ (x[:4],ids(x)) for x in adj[p] if x in S])
"
```

```bash
cd /tmp/w && python3 -c "
import sys;sys.path.insert(0,'/tmp/w');from ev import *
print(ev([k for k,v in d.items() if v<=8]))
print(ev([k for k,v in d.items() if 8<=v<=11]))
"
```

```bash
cd /tmp/w && cat > stats.py <<'EOF'
import sys,json;sys.path.insert(0,'/tmp/w');from ev import *
def st(S):
  S=set(S);m=sum(1 for u in S for v in adj[u] if v in S)//2;b=sum(1 for u in S for v in adj[u] if v not in S)
  tri=sum(1 for u in S for v in adj[u] if v in S for w in adj[v] if w in S and w in adj[u])//6
  vol=sum(len(adj[u]) for u in S)
  return dict(n=len(S),m=m,b=b,tri=tri,cond=round(b/vol,3),avgdeg=round(2*m/len(S),2),dens=round(2*m/len(S)/(len(S)-1),3) if len(S)>1 else 0)
EOF
python3 -c "
import sys,json;sys.path.insert(0,'/tmp/w');from stats import *
far=[k for k,v in d.items() if
```

```bash
cd /tmp/w && python3 -c "
import sys;sys.path.insert(0,'/tmp/w');from ev import *
far=[k for k,v in d.items() if v==20]
print(ev([far[0],far[5],far[10]]))
print(ev(['b8926eb97b','40234ca2ac','02ac8fd827']))
print(ev(['b8926eb97b',far[5],far[10]]))
"
```

```bash
cd /tmp/w && pip list 2>/dev/null | grep -i networkx; python3 -c "
import sys;sys.path.insert(0,'/tmp/w');from ev import *
import networkx as nx
G=nx.Graph([(u,v) for u in adj for v in adj[u]])
s='b8926eb97b'
core=nx.core_number(G);print('start core',core[s],{k:sum(1 for x in core.values() if x==k) for k in set(core.values())})
print('tri start',nx.triangles(G,s),'clust',nx.clustering(G,s))
for k in [2,3]:
  H=G.subgraph([n for n in G if core[n]>=k]); c=nx.node_connected_component(H,s) if s in H else set(); print(k,len(c))
print(len(G.edges()), nx.number_connected_components(G))
"
```

```bash
cd /tmp/w && python3 -c "
import sys;sys.path.insert(0,'/tmp/w');from ev import *
import networkx as nx
G=nx.Graph([(u,v) for u in adj for v in adj[u]])
far=[k for k,v in d.items() if v==20]
for x in ['b8926eb97b','40234ca2ac','e6f6a117af','02ac8fd827','491b1446f4',far[0],adj[far[0]][0],far[5],far[10]]: print(x,G.degree(x),nx.triangles(G,x),round(nx.clustering(G,x),3))
"
```

```bash
cd /tmp/w && cat > wl.py <<'EOF'
import sys,json,math,collections,itertools;sys.path.insert(0,'/tmp/w');from ev import *
s='b8926eb97b'
def feats(S,H):
    S=set(S);lab={u:('S' if u==s else 'n') for u in S};F=[collections.Counter(lab.values())]
    for h in range(H):
        lab={u:(lab[u],tuple(sorted(lab[v] for v in adj[u] if v in S))) for u in S}
        # compress
        lab={u:hash(l) for u,l in lab.items()}
        F.append(collections.Counter(lab.values()))
    return F
def kern(FA,FB,mode):
    if mode=='sum':
        dot=sum(sum(a[k]*b.get(k,0) for k in a) for a,b in zip(FA,FB))
    
```

**agent:** The WL model reproduces the observed pattern (H≈3, summed kernel). Now I'll collect every past evaluation I can reconstruct and search offline for a target T that fits them all.

```bash
cd /tmp/w && cat > obs.py <<'EOF'
import sys,json;sys.path.insert(0,'/tmp/w');from wl import *
far=[k for k,v in d.items() if v==20];x=far[0]
D=lambda f:[k for k,v in d.items() if f(v)]
obs=[([s],.0148),([x],.4154),([s,'40234ca2ac'],.3042),(['162d0abeba','610a9500ea','8bedf3e222'],.5192),(['162d0abeba','252693b05c','439e9f1003'],.5451),([s,'40234ca2ac','02ac8fd827'],.4599),([s,far[5],far[10]],.3782),
(ball(s,1),.4066),(ball(s,2),.833),(ball(s,3),.9024),(ball(s,4),.8952),(ball(x,1),.7612),(ball(x,2),.8941),(ball(x,3),.9178),(ball(x,4),.9089),(ball(far[1],3),.9174),(ball(x,3)+[s],.9157),(ball(x,
```

```bash
cd /tmp/w && cat > sa.py <<'EOF'
import sys,random,math;sys.path.insert(0,'/tmp/w');from obs import *
H=int(sys.argv[1]);random.seed(int(sys.argv[2]))
OF=[(feats(S,H),o) for S,o in obs]
def E(T):
    FT=feats(T,H);return sum((kern(f,FT,'sum')-o)**2 for f,o in OF)
cand=[k for k,v in d.items() if v<=6]
T=set(ball(s,3));e=E(T);bestT,beste=set(T),e
temp=0.01
for it in range(6000):
    m=random.choice(cand)
    if m==s: continue
    T2=T^{m}
    e2=E(T2)
    if e2<e or random.random()<math.exp((e-e2)/temp):
        T,e=T2,e2
        if e<beste: bestT,beste=set(T),e
    temp*=0.999
print(H,beste,len
```

```bash
cd /tmp/w && sed -i 's/range(6000)/range(int(sys.argv[3]))/; s/temp\*=0.999/temp*=0.9995/' sa.py && for H in 2 3 4 5; do for sd in 1 2; do (python3 sa.py $H $sd 12000 | cut -c1-60) & done; done; wait
```

**agent:** The fit is best at H=3, but the singleton ratio pins |T| = 29, while the unconstrained search drifted to about 55 nodes. Rerunning the search with the target size fixed at 29.

```bash
cd /tmp/w && cat > sa2.py <<'EOF'
import sys,random,math;sys.path.insert(0,'/tmp/w');from obs import *
H=int(sys.argv[1]);random.seed(int(sys.argv[2]));N=int(sys.argv[4])
OF=[(feats(S,H),o) for S,o in obs]
def E(T):
    FT=feats(T,H);return sum((kern(f,FT,'sum')-o)**2 for f,o in OF)
cand=[k for k,v in d.items() if 1<=v<=5]
T=set(sorted(ball(s,4),key=lambda k:d[k])[:N]);e=E(T);bestT,beste=set(T),e
temp=0.01
for it in range(int(sys.argv[3])):
    a=random.choice(list(T-{s}));b=random.choice(cand)
    if b in T: continue
    T2=(T-{a})|{b}
    e2=E(T2)
    if e2<e or random.random()<math.exp((e-e
```

```bash
cd /tmp/w && python3 -c "
import sys,json;sys.path.insert(0,'/tmp/w');from obs import *
T=json.load(open('T_3_29_1.json'));FT=feats(T,3)
r=[(round(kern(feats(S,3),FT,'sum')-o,4),i,len(S),o) for i,(S,o) in enumerate(obs)]
for x in sorted(r,key=lambda x:-abs(x[0]))[:15]: print(x)
print(sorted((d[k],k[:4]) for k in T))
import networkx as nx
G=nx.Graph([(u,v) for u in adj for v in adj[u]]);print(nx.is_connected(G.subgraph(T)))
"
```

```bash
cd /tmp/w && cat > bf.py <<'EOF'
import sys,itertools;sys.path.insert(0,'/tmp/w');from obs import *
H=3;OF=[(feats(S,H),o) for S,o in obs]
def E(T):
    FT=feats(T,H);return sum((kern(f,FT,'sum')-o)**2 for f,o in OF)
b3=ball(s,3);d4=[k for k,v in d.items() if v==4]
r=sorted((E(b3+list(c)),c) for c in itertools.combinations(d4,3))
for x in r[:5]: print(x)
EOF
python3 bf.py
```

```bash
cd /tmp/w && cat > cands.py <<'EOF'
import sys,itertools;sys.path.insert(0,'/tmp/w');from obs import *
H=3;OF=[(feats(S,H),o) for S,o in obs]
def E(T):
    FT=feats(T,H);return sum((kern(f,FT,'sum')-o)**2 for f,o in OF)
import networkx as nx
G=nx.Graph([(u,v) for u in adj for v in adj[u]])
C={}
C['bfs29']=list(d)[:29]
order=sorted(d,key=lambda k:(d[k],k));C['bfsid29']=order[:29]
# greedy: add neighbor with most links to current set
T={s}
while len(T)<29:
    fr={v for u in T for v in adj[u] if v not in T}
    T.add(max(sorted(fr),key=lambda v:sum(w in T for w in adj[v])))
C['greedy']=list(T)
#
```

```bash
cd /tmp/w && sed -i 's/^pr=nx.pagerank.*$/pr=nx.pagerank_python(G,personalization={s:1}) if hasattr(nx,"pagerank_python") else None\nif pr: C["ppr29"]=sorted(pr,key=lambda k:-pr[k])[:29]/' cands.py && python3 cands.py
```

**agent:** No simple ordering rule (BFS, DFS, greedy) fits exactly. Running a longer constrained search to try to drive the fit error to near zero.

```bash
cd /tmp/w && nproc && sed -i 's/^T=set(sorted(ball(s,4),key=lambda k:d\[k\])\[:N\])/T=set(json.load(open(sys.argv[5]))) if len(sys.argv)>5 else set(sorted(ball(s,4),key=lambda k:d[k])[:N])/; s/^temp=0.01/temp=float(sys.argv[6]) if len(sys.argv)>6 else 0.01/' sa2.py && sed -i '1a import json' sa2.py && time (for sd in 11 12 13 14; do (python3 sa2.py 3 $sd 40000 29 T_3_29_1.json 0.002 | cut -c1-30) & done; wait)
```

```bash
cd /tmp/w && python3 -c "
import sys,json;sys.path.insert(0,'/tmp/w');from obs import *
T=json.load(open('T_3_29_12.json'));FT=feats(T,3)
r=[(round(kern(feats(S,3),FT,'sum')-o,4),i,len(S),o) for i,(S,o) in enumerate(obs)]
print(sorted(abs(x[0]) for x in r))
print(sorted(r,key=lambda x:-abs(x[0]))[:6])
print(FT[0],sum(sum(v*v for v in f.values()) for f in FT), [sorted(f.values(),reverse=True) for f in FT])
"
```

```bash
cd /tmp/w && sed -i 's/^def E(T):\n.*//' sa2.py && python3 - <<'EOF'
src=open('/tmp/w/sa2.py').read()
src=src.replace("""def E(T):
    FT=feats(T,H);return sum((kern(f,FT,'sum')-o)**2 for f,o in OF)""","""W=[50 if len(S)<=6 else 1 for S,o in obs]
def E(T):
    FT=feats(T,H);nT=sum(sum(v*v for v in f.values()) for f in FT)
    return sum(w*(kern(f,FT,'sum')-o)**2 for w,(f,o) in zip(W,OF))+1e-5*(nT-1136)**2""")
open('/tmp/w/sa3.py','w').write(src)
EOF
for sd in 21 22 23 24 25 26; do (python3 sa3.py 3 $sd 40000 29 T_3_29_12.json 0.003 | cut -c1-30) & done; wait
```

```bash
cd /tmp/w && cat >> cands.py <<'EOF'
C={}
deg={u:len(adj[u]) for u in adj}
for nm,f in [('deg==4',lambda u:deg[u]==4),('deg>=4',lambda u:deg[u]>=4),('deg<=4',lambda u:deg[u]<=4),('deg in34',lambda u:deg[u] in(3,4)),('deg in45',lambda u:deg[u] in(4,5))]:
    H2=G.subgraph([u for u in G if f(u)]);c=nx.node_connected_component(H2,s);print(nm,len(c));C[nm]=list(c)
for k,v in C.items():
    if len(v)<=200: print(k,len(v),E(v))
EOF
python3 cands.py 2>&1 | tail -12
```

```bash
probe evaluate b8926eb97b 40234ca2ac 7177bc61e3; probe evaluate b8926eb97b 40234ca2ac 7177bc61e3 91b3c0bda3
```

**agent:** Stars around the start show it has exactly **2** neighbors inside T. Searching filtered-neighborhood rules that produce |T| = 29 with the start's T-degree equal to 2.

```bash
cd /tmp/w && cat > rules.py <<'EOF'
import sys;sys.path.insert(0,'/tmp/w');from obs import *
import networkx as nx
G=nx.Graph([(u,v) for u in adj for v in adj[u]])
H=3;OF=[(feats(S,H),o) for S,o in obs]
def E(T):
    FT=feats(T,H);return sum((kern(f,FT,'sum')-o)**2 for f,o in OF)
deg=dict(G.degree());tri=nx.triangles(G);core=nx.core_number(G);cl=nx.clustering(G)
for n in adj[s]: print(n,deg[n],tri[n],core[n],round(cl[n],2))
attrs={'deg':deg,'tri':tri,'core':core}
out=[]
for an,a in attrs.items():
  for op in ['>=','<=','==']:
    for t in sorted(set(a.values())):
      ok=lambda u:eval(f'a[u]{
```

```bash
cd /tmp/w && cat > balls.py <<'EOF'
import sys;sys.path.insert(0,'/tmp/w');from obs import *
H=3;OF=[(feats(S,H),o) for S,o in obs]
def E(T):
    FT=feats(T,H);return sum((kern(f,FT,'sum')-o)**2 for f,o in OF)
res=[]
for c in [k for k,v in d.items() if v<=8]:
    for r in range(1,9):
        T=ball(c,r)
        if len(T)>40: break
        if s in T and 26<=len(T)<=32: res.append((E(T),c,r,len(T),d[c],sum(v in T for v in adj[s])))
res.sort();print(res[:8])
EOF
python3 balls.py
```

```bash
cd /tmp/w && cat >> rules.py <<'EOF'
print('---')
for an,a in attrs.items():
  for op in ['>=','<=','==']:
    for t in sorted(set(a.values())):
      ok=lambda u:eval(f'a[u]{op}t') or u==s
      Hs=G.subgraph([u for u in G if ok(u)])
      c=nx.node_connected_component(Hs,s)
      if len(c)<=60: print(an,op,t,len(c),sum(v in c for v in adj[s]),round(E(list(c)),4))
EOF
python3 rules.py | sed -n '/---/,$p'
```

```bash
cd /tmp/w && cat > intv.py <<'EOF'
import sys;sys.path.insert(0,'/tmp/w');from obs import *
H=3;OF=[(feats(S,H),o) for S,o in obs]
def E(T):
    FT=feats(T,H);return sum((kern(f,FT,'sum')-o)**2 for f,o in OF)
import collections
def bfs(c):
    D={c:0};q=collections.deque([c])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in D: D[v]=D[u]+1;q.append(v)
    return D
res=[]
for X in adj:
    DX=bfs(X);L=DX[s]
    T=[u for u in adj if d[u]+DX[u]==L]
    if 20<=len(T)<=40: res.append((E(T),X,len(T),L,sum(v in T for v in adj[s])))
res.sort();print(res[:8])
EOF
pytho
```

```bash
cd /tmp/w && python3 -c "
import sys,collections;sys.path.insert(0,'/tmp/w');from ev import *
X='7718202434';D={X:0};q=collections.deque([X])
while q:
    u=q.popleft()
    for v in adj[u]:
        if v not in D: D[v]=D[u]+1;q.append(v)
T=[u for u in adj if d[u]+D[u]==D['b8926eb97b']]
open('final.txt','w').write('\n'.join(T));print(len(T))
"; probe evaluate - < final.txt
```

**agent:** Score 1.0. Submitting.

```bash
probe submit - < /tmp/w/final.txt
```

**agent:** I submitted a 29-item selection and it was accepted. It scored 1.0 on `evaluate` just before submitting, and I used 106 of the 150 evaluate calls.

**The rule:** the target is every item that lies on some shortest path between the start item `b8926eb97b` and item `7718202434`, which is 11 links away.

How I got there:
1. **Mapped the whole system.** `neighbors` is free, so I crawled all 1,599 items. They all connect into one network.
2. **Worked out what `evaluate` measures.** The score barely depends on location. Groups of nearby items centred far from the start scored about as well as groups around the start, and any single item other than the start scored exactly 0.4154. The numbers fit a structural similarity measure (a Weisfeiler-Lehman graph kernel, run 3 rounds). It compares the link pattern within my selection to the link pattern within the target, with the start item marked as special. Under that model:
   - comparing the start alone with any other single item pinned the target at **29 items**;
   - small test groups showed the target contains exactly 2 of the start's 4 neighbors, so it isn't a "everything within N links" region.
3. **Fitted the model offline.** I rebuilt the measure locally and checked candidate rules against all 88 past evaluations at no cost. Simple neighbourhood regions, ordered walks and filters by item properties did not fit. "Items on shortest paths from the start to some item X" fitted exactly for X = `7718202434`, with an error of about 1e-7.

