# sp-opus55-b2 / hidden-pattern-probe__EadoGSQ

model=bedrock/us.anthropic.claude-opus-5-5 reward=0.0 exception=AgentTimeoutError evaluate=80 best=0.9612

```bash
probe --help; probe status
```

**agent:** Let me BFS the graph fully (neighbors is free).

```bash
probe neighbors b8926eb97b; mkdir -p /tmp/w && cat > /tmp/w/bfs.py <<'EOF'
import json,subprocess,collections
s="b8926eb97b"
adj={};dist={s:0};q=collections.deque([s])
while q:
    u=q.popleft()
    out=json.loads(subprocess.check_output(["probe","neighbors",u]))
    nb=out if isinstance(out,list) else out.get("neighbors",out)
    adj[u]=nb
    for v in nb:
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
    if len(dist)>5000: break
json.dump({"adj":adj,"dist":dist},open("/tmp/w/g.json","w"))
print(len(dist),collections.Counter(dist.values()))
EOF
python3 /tmp/w/bfs.py
```

```bash
cd /tmp/w && python3 -c "
import json,collections
g=json.load(open('g.json'));adj=g['adj'];d=g['dist']
asym=sum(1 for u in adj for v in adj[u] if u not in adj.get(v,[]))
print('asym',asym)
print(collections.Counter(len(v) for v in adj.values()))
for r in range(5): print(r,sum(1 for x in d.values() if x<=r))
"
for r in 1 2 3; do python3 -c "
import json;d=json.load(open('/tmp/w/g.json'))['dist']
print('\n'.join(k for k,v in d.items() if v<=$r))" | probe evaluate -; done
```

```bash
for r in 4 5; do python3 -c "
import json;d=json.load(open('/tmp/w/g.json'))['dist']
print('\n'.join(k for k,v in d.items() if v<=$r))" | probe evaluate -; done
```

```bash
for r in 6 7 8 10; do python3 -c "
import json;d=json.load(open('/tmp/w/g.json'))['dist']
s=[k for k,v in d.items() if v<=$r];print(len(s)>200 and '' or '\n'.join(s))" | probe evaluate -; done
```

```bash
probe evaluate b8926eb97b; for n in 40234ca2ac 7177bc61e3 91b3c0bda3 e6f6a117af; do probe evaluate b8926eb97b $n; done
```

```bash
cd /tmp/w; python3 -c "
import json;g=json.load(open('g.json'));d=g['dist']
for r in [2,3,10,30]: print(r,[k for k,v in d.items() if v==r][:2])
print(g['adj']['40234ca2ac'])"
```

```bash
probe evaluate b8926eb97b 02ac8fd827; probe evaluate b8926eb97b 491b1446f4; probe evaluate b8926eb97b 7c68283178; probe evaluate 40234ca2ac
```

```bash
probe evaluate b8926eb97b; probe evaluate 7c68283178; probe evaluate 40234ca2ac 7177bc61e3
```

```bash
cd /tmp/w; python3 -c "
import json,random;g=json.load(open('g.json'));d=g['dist']
random.seed(1);ks=[k for k in d if d[k]>20];random.shuffle(ks)
json.dump(ks,open('far.json','w'))"
for n in 3 5 10 50; do python3 -c "import json;print('\n'.join(json.load(open('/tmp/w/far.json'))[:$n]))" | probe evaluate -; done
```

```bash
for n in 2 3 10 50; do (echo b8926eb97b; python3 -c "import json;print('\n'.join(json.load(open('/tmp/w/far.json'))[:$n]))") | probe evaluate -; done
```

```bash
for n in 20 30 50 100 200; do python3 -c "import json;print('\n'.join(json.load(open('/tmp/w/far.json'))[:$n]))" | probe evaluate -; done
```

```bash
cd /tmp/w; python3 -c "
import json;d=json.load(open('g.json'))['dist'];f=json.load(open('far.json'))
b=[k for k,v in d.items() if v<=5];print(len(b))
open('b5','w').write('\n'.join(b));open('b5f','w').write('\n'.join(b+f[:10]));open('b5f50','w').write('\n'.join(b+f[:50]))"
probe evaluate - < b5f; probe evaluate - < b5f50
```

```bash
cd /tmp/w; python3 -c "
import json,collections;g=json.load(open('g.json'));d=g['dist'];a=g['adj']
for r in range(1,7):
  print(r,collections.Counter(len(a[k]) for k,v in d.items() if v==r))
"
```

```bash
cd /tmp/w; python3 -c "
import json;d=json.load(open('g.json'))['dist']
b=[k for k,v in d.items() if v<=2 and v>0];open('b2ns','w').write('\n'.join(b))
b=[k for k,v in d.items() if v<=5 and v>0];open('b5ns','w').write('\n'.join(b))"
probe evaluate - < b2ns; probe evaluate - < b5ns
```

```bash
cd /tmp/w; for r in 2 3 4 5; do python3 -c "
import json;d=json.load(open('g.json'))['dist']
print('\n'.join(k for k,v in d.items() if v==$r))" | probe evaluate -; done
```

```bash
cd /tmp/w; for r in 1 3 4 6 7 8; do python3 -c "
import json;d=json.load(open('g.json'))['dist']
print('\n'.join(k for k,v in d.items() if 0<v<=$r))" | probe evaluate -; done
```

```bash
probe evaluate 40234ca2ac 02ac8fd827; probe evaluate 40234ca2ac 02ac8fd827 0d66623d41; probe evaluate 40234ca2ac 02ac8fd827 0d66623d41 aaf16439e9
```

```bash
cd /tmp/w; python3 -c "
import json;g=json.load(open('g.json'));a=g['adj'];d=g['dist']
c=[k for k in d if d[k]==30 and len(a[k])==4][0]
print(c,' '.join(a[c][:3]), [len(a[x]) for x in a[c]], [d[x] for x in a[c]])
print([len(a[x]) for x in ['40234ca2ac','02ac8fd827','0d66623d41','aaf16439e9']])"
```

```bash
probe evaluate 7c68283178 05dbfe13bb 6dcdb5c81f 887ce8c272
```

```bash
cd /tmp/w; cat > cand.py <<'EOF'
import json,collections
g=json.load(open('g.json'));a=g['adj'];d=g['dist'];s="b8926eb97b"
def comp(pred):
    seen={s};q=[s]
    while q:
        u=q.pop()
        for v in a[u]:
            if v not in seen and pred(v): seen.add(v);q.append(v)
    return seen
C={}
for k in range(1,8):
    C[f'deg=={k}']=comp(lambda v:len(a[v])==k)
    C[f'deg>={k}']=comp(lambda v:len(a[v])>=k)
    C[f'deg<={k}']=comp(lambda v:len(a[v])<=k)
# k-core
def core(k):
    alive=set(a);ch=True
    while ch:
        ch=False
        for u in list(alive):
            if sum(v in alive f
```

```bash
cd /tmp/w; python3 -c "
import json;print('\n'.join(json.load(open('cands.json'))['deg==4']))" | probe evaluate -
```

```bash
cd /tmp/w; python3 -c "
import json;g=json.load(open('g.json'));a=g['adj']
def ind(S):
  return [(u,v) for i,u in enumerate(S) for v in S[i+1:] if v in a[u]]
for S in [['40234ca2ac','02ac8fd827','0d66623d41','aaf16439e9'],['7c68283178','05dbfe13bb','6dcdb5c81f','887ce8c272']]:
  print(ind(S),[len(a[x]) for x in S])
# triangles count
t=sum(1 for u in a for v in a[u] for w in a[v] if w in a[u])//6
print('triangles',t)
"
```

**agent:** The score looks structural: it's location-independent and fits a cosine similarity of node-label histograms, where the start node gets its own label. I'm fitting that model to the data so far.

```bash
cd /tmp/w; cat > fit.py <<'EOF'
import json,numpy as np,collections
g=json.load(open('g.json'));a={k:set(v) for k,v in g['adj'].items()};d=g['dist'];s="b8926eb97b"
far=json.load(open('far.json'))
def ball(r,st=True): return [k for k,v in d.items() if v<=r and (st or v>0)]
obs=[]
for r,sc in [(1,.4066),(2,.833),(3,.9024),(4,.8952),(5,.9339),(6,.9096),(7,.9249),(8,.9329)]: obs.append((ball(r),sc))
for r,sc in [(1,.4154),(2,.9041),(3,.9132),(4,.9076),(5,.9383),(6,.9144),(7,.9283),(8,.9352)]: obs.append((ball(r,False),sc))
for r,sc in [(2,.6079),(3,.6756),(4,.6246),(5,.5404)]: obs.append(([k for k
```

```bash
cd /tmp/w; cat > shapes.py <<'EOF'
import json,itertools,random
g=json.load(open('g.json'));a={k:set(v) for k,v in g['adj'].items()};d=g['dist']
random.seed(5)
far=[k for k in d if d[k]>15]
def ind(S): return sorted(tuple(sorted((S.index(u),S.index(v)))) for u in S for v in S if u<v and v in a[u])
res={}
# find P3 (non-triangle wedge), triangle, P4 induced, K1,3 induced (claw)
for u in far:
    nb=[v for v in a[u] if v in d and d[v]>15]
    for x,y in itertools.combinations(nb,2):
        if y not in a[x]: res.setdefault('P3',[]).append([x,u,y])
        else: res.setdefault('K3',[]).append([u,
```

```bash
cd /tmp/w; python3 -c "
import json;g=json.load(open('g.json'));a={k:set(v) for k,v in g['adj'].items()};r=json.load(open('shapes.json'))
def sep(A,B): return not any(v in a[u] or u==v for u in A for v in B)
def two(k):
  L=r[k];A=L[0]
  for B in L[1:]:
    if sep(A,B): return A+B
for k in ['P3','K3','claw']: print(k,' '.join(r[k][0]),'|',' '.join(two(k)))
"
```

```bash
for S in "e3d5481d23 44fb37a220 fd25d1841d" "e3d5481d23 44fb37a220 fd25d1841d 4821f7f34b 5711798f28 1e136b10fb" "81d32c4d0b a0fa59710b 25fe256a0c" "81d32c4d0b a0fa59710b 25fe256a0c 1e136b10fb c4d1f796e6 905b506544" "44fb37a220 e3d5481d23 fd25d1841d adc8da07b3"; do probe evaluate $S; done
```

```bash
cd /tmp/w; python3 -c "
import json;g=json.load(open('g.json'));a={k:set(v) for k,v in g['adj'].items()};r=json.load(open('shapes.json'));f=json.load(open('far.json'))
P=r['P3'][0];T=r['K3'][0]
iso=[x for x in f if not any(x==u or x in a[u] for u in P+T)]
print(' '.join(P+iso[:1]));print(' '.join(P+iso[:3]));print(' '.join(P+T))"
```

```bash
probe evaluate e3d5481d23 44fb37a220 fd25d1841d 4b4c6525bc; probe evaluate e3d5481d23 44fb37a220 fd25d1841d 4b4c6525bc 08628c9217 019fc18178; probe evaluate e3d5481d23 44fb37a220 fd25d1841d 81d32c4d0b a0fa59710b 25fe256a0c
```

```bash
python3 -c "
from scipy.optimize import fsolve
import numpy as np
def F(z):
  P,c=z
  return [(.5451*P+.4154)/np.sqrt(P*P+2*c+1)-.6004,(.5451*P+1.2462)/np.sqrt(P*P+6*c+9)-.5845]
for g in [(1,0),(3,0),(0.5,0.1),(5,1)]:
  s=fsolve(F,g,full_output=1);print(s[0],s[2])
"
```

```bash
python3 -c "
import numpy as np
best=[]
for P in np.linspace(0.05,10,2000):
  for c in np.linspace(-1,3,801):
    if P*P+2*c+1<=0: continue
    e1=(.5451*P+.4154)/np.sqrt(P*P+2*c+1)-.6004
    if P*P+6*c+9<=0: continue
    e2=(.5451*P+1.2462)/np.sqrt(P*P+6*c+9)-.5845
    best.append((abs(e1)+abs(e2),P,c))
best.sort();print(best[:5])"
```

```bash
cd /tmp/w; cat > wl.py <<'EOF'
import json,collections,numpy as np
g=json.load(open('g.json'));A={k:set(v) for k,v in g['adj'].items()};d=g['dist'];s="b8926eb97b"
def wl(S,h=3,startlab=True):
    S=set(S);lab={u:('s' if (u==s and startlab) else 'x') for u in S}
    c=collections.Counter((0,l) for l in lab.values())
    for i in range(1,h+1):
        lab={u:(lab[u],tuple(sorted(lab[v] for v in A[u]&S))) for u in S}
        lab={u:hash(l) for u,l in lab.items()}
        c.update((i,l) for l in lab.values())
    return c
def cos(a,b):
    return sum(a[k]*b.get(k,0) for k in a)/np.sqrt(sum(x*x for
```

```bash
cd /tmp/w; cat > search.py <<'EOF'
exec(open('check.py').read().split('V=[wl')[0])
import itertools
def err(T):
    vt=wl(T);return max(abs(cos(wl(S),vt)-sc) for S,sc in obs)
cands={}
ball=lambda c,r: {k for k in A if k==c} | set()
def bfs(src,r):
    dist={src:0};q=[src]
    for u in q:
        if dist[u]<r:
            for v in A[u]:
                if v not in dist: dist[v]=dist[u]+1;q.append(v)
    return dist
b3=set(bfs(s,3));b4=set(bfs(s,4))
cands['b3']=b3;cands['b4']=b4
# nodes in b4 with >=k neighbors in b3
for k in range(1,5): cands[f'b3+{k}']=b3|{v for v in b4-b3 if len(A[v]&b3)>=k}

```

```bash
cd /tmp/w; cat > sa.py <<'EOF'
exec(open('search.py').read().split('for name,T')[0])
import random,math,sys
random.seed(int(sys.argv[1]))
VS=[(wl(S),sc) for S,sc in obs]
def E(T):
    vt=wl(T);return sum((cos(v,vt)-sc)**2 for v,sc in VS)
pool=set(bfs(s,7))
T=set(cands['b3+2']);T=set(list(T))
def conn(T):
    seen={s};q=[s]
    for u in q:
        for v in A[u]&T:
            if v not in seen: seen.add(v);q.append(v)
    return len(seen)==len(T)
cur=E(T);best=(cur,set(T));temp=1e-3
for it in range(20000):
    N=set(T);r=random.random()
    if r<0.4 or len(N)<29:
        bd=[v for u in N for v i
```

```bash
cd /tmp/w; python3 -c "
import json,collections;d=json.load(open('g.json'))['dist']
for i in [1,2,3,4]:
  b=json.load(open(f'best{i}.json'));print(i,sorted(collections.Counter(d[x] for x in b).items()))
b3=[k for k in d if d[k]<=3]
sets=[set(json.load(open(f'best{i}.json'))) for i in [1,2,3,4]]
print('common',len(set.intersection(*sets)), 'b3 in all', len(set(b3)&set.intersection(*sets)))
"; probe evaluate - < <(python3 -c "import json;print('\n'.join(json.load(open('/tmp/w/best1.json'))))")
```

```bash
cd /tmp/w; python3 - <<'EOF'
import json
exec(open('search.py').read().split('for name,T')[0])
T=cands['b3+2'];open('c_b32','w').write('\n'.join(T))
vt=wl(json.load(open('best1.json')))
print([round(cos(wl(S),vt),4) for S in [T]])
EOF
probe evaluate - < c_b32
```

```bash
cd /tmp/w; python3 - <<'EOF'
import json
ex=[(json.load(open('best1.json')),.945),(open('c_b32').read().split('\n'),.9214)]
json.dump(ex,open('extra.json','w'))
EOF
cat > sa2.py <<'EOF'
exec(open('search.py').read().split('for name,T')[0])
import random,math,sys
seed=int(sys.argv[1]);random.seed(seed)
obs+= [(S,sc) for S,sc in json.load(open('extra.json'))]
VS=[(wl(S),sc) for S,sc in obs]
def E(T):
    vt=wl(T);return sum((cos(v,vt)-sc)**2 for v,sc in VS)
def conn(T):
    seen={s};q=[s]
    for u in q:
        for v in A[u]&T:
            if v not in seen: seen.add(v);q.append(v)
    return le
```

```bash
cd /tmp/w; python3 - <<'EOF'
import json,collections
exec(open('wl.py').read())
def bfs(src,r):
    dist={src:0};q=[src]
    for u in q:
        if dist[u]<r:
            for v in A[u]:
                if v not in dist: dist[v]=dist[u]+1;q.append(v)
    return dist
def hist(T):
    T=set(T);return sorted(collections.Counter((len(A[u]&T), s in A[u]) for u in T if u!=s).items()), len(A[s]&T)
for r in [2,3,4]: print(r,hist(bfs(s,r)))
for i in [1,12,14]: print(i,hist(json.load(open(f'best{i}.json'))))
EOF
```

```bash
cd /tmp/w; python3 -c "
exec(open('wl.py').read())
N=sorted(A[s]);print(N,[(u,v) for u in N for v in N if u<v and v in A[u]], [len(A[u]) for u in N])"
```

```bash
probe evaluate b8926eb97b 40234ca2ac 7177bc61e3 91b3c0bda3; probe evaluate b8926eb97b 40234ca2ac 7177bc61e3
```

**agent:** Probes show the start node has exactly 2 neighbors inside the target, so the target isn't a plain ball. Two of start's neighbors have degree 4 like start does. Testing rules based on degree.

```bash
cd /tmp/w; python3 - <<'EOF'
import json
exec(open('wl.py').read())
for r in range(1,12):
    T=[k for k,v in d.items() if v<=r and len(A[k])==4]
    print(r,len(T))
EOF
```

```bash
cd /tmp/w; python3 - <<'EOF'
import json
ex=json.load(open('extra.json'))
s="b8926eb97b"
ex+= [([s,'40234ca2ac','7177bc61e3','91b3c0bda3'],.3987),([s,'40234ca2ac','7177bc61e3'],.3848)]
json.dump(ex,open('extra.json','w'))
EOF
sed -i 's/range(12000)/range(int(sys.argv[4]) if len(sys.argv)>4 else 12000)/' sa2.py
for i in 21 22 23 24 25 26; do timeout 1500 python3 sa2.py $i best12.json 1e-3 25000 & done; wait
```

```bash
cd /tmp/w; python3 - <<'EOF'
exec(open('sa2.py').read().split('def conn')[0].replace('seed=int(sys.argv[1]);',''))
vt=wl(json.load(open('best12.json')))
for i,(v,sc) in enumerate(VS): print(i,len(obs[i][0]),sc,round(cos(v,vt),4))
EOF
```

```bash
cd /tmp/w; python3 - <<'EOF'
import sys;sys.argv=['x','0']
exec(open('sa2.py').read().split('def conn')[0])
vt=wl(json.load(open('best12.json')))
for i,(v,sc) in enumerate(VS): print(i,len(obs[i][0]),sc,round(cos(v,vt),4))
EOF
```

```bash
cd /tmp/w; python3 - <<'EOF'
import sys;sys.argv=['x','0']
exec(open('sa2.py').read().split('def conn')[0])
import collections
def rep(name,T):
    vt=wl(T);e=max(abs(cos(v,vt)-sc) for v,sc in VS)
    if e<0.03: print(name,len(T),round(e,5))
for r in range(1,9):
  for op in ['==','>=','<=']:
    for k in range(2,7):
      T=[x for x,v in d.items() if v<=r and (x==s or eval(f'{len(A[x])}{op}{k}'))]
      rep(f'r{r} deg{op}{k}',T)
print('done')
EOF
```

```bash
cd /tmp/w; for i in 12 2 3 4 11 13 14; do echo -n "$i "; python3 -c "import json;print('\n'.join(json.load(open('best$i.json'))))" | probe evaluate -; done
```

```bash
cd /tmp/w; python3 - <<'EOF'
import json
ex=json.load(open('extra.json'))
for i,sc in [(12,.9534),(2,.9541),(3,.9586),(4,.943),(11,.9571),(13,.9547),(14,.9598)]:
    ex.append((json.load(open(f'best{i}.json')),sc))
json.dump(ex,open('extra.json','w'))
EOF
for i in 31 32 33 34 35 36; do timeout 1500 python3 sa2.py $i best14.json 3e-3 25000 & done; wait
```

```bash
cd /tmp/w; python3 - <<'EOF'
import itertools,json
exec(open('wl.py').read())
far=[k for k in d if d[k]>15]
out={}
for u in far:
    nb=[v for v in A[u] if d[v]>15]
    for k in [4,5]:
        for c in itertools.combinations(nb,k):
            if all(y not in A[x] for x,y in itertools.combinations(c,2)): out.setdefault(f'K1{k}',[u,*c])
# start-adjacent stars
for n in A[s]:
    nb=[v for v in A[n] if v!=s and v not in A[s]]
    for k in range(0,5):
        for c in itertools.combinations(nb,k):
            if all(y not in A[x] for x,y in itertools.combinations(c,2)): out.setdefault(f'S{k}',[s,n
```

```bash
cd /tmp/w; for k in K14 K15 S1 S2 S3; do echo -n "$k "; python3 -c "import json;print('\n'.join(json.load(open('probes.json'))['$k']))" | probe evaluate -; done
```

```bash
cd /tmp/w; python3 - <<'EOF'
import json,numpy as np
exec(open('wl.py').read())
P=json.load(open('probes.json'))
Tn=33.78; Tx=28; Ts=1
for k,sc in [('K14',.5003),('K15',.4668),('S1',.4599),('S2',.4822),('S3',.4741)]:
    v=wl(P[k]);nrm=np.sqrt(sum(x*x for x in v.values()))
    base=(len(P[k])-(s in P[k]))*Tx+(s in P[k])*Ts
    print(k,round(sc*nrm*Tn-base,2))
EOF
```

```bash
cd /tmp/w; cat > dec.py <<'EOF'
import json,numpy as np,sys
exec(open('wl.py').read())
P=json.load(open('probes.json'))
r=json.load(open('shapes.json'))
P.update({'P3':r['P3'][0],'K3':r['K3'][0],'claw':r['claw'][0],'paw':['7c68283178','05dbfe13bb','6dcdb5c81f','887ce8c272']})
Tn=float(sys.argv[1]); Tx=28; Ts=1
for k,sc in [('K14',.5003),('K15',.4668),('S1',.4599),('S2',.4822),('S3',.4741),('P3',.5451),('K3',.5192),('claw',.5468),('paw',.7174)]:
    v=wl(P[k]);nrm=np.sqrt(sum(x*x for x in v.values()))
    base=(len(P[k])-(s in P[k]))*Tx+(s in P[k])*Ts
    print(k,round(sc*nrm*Tn-base,2),round(n
```

```bash
cd /tmp/w; python3 - <<'EOF'
import json
ex=json.load(open('extra.json'))
P=json.load(open('probes.json'))
for k,sc in [('K14',.5003),('K15',.4668),('S1',.4599),('S2',.4822),('S3',.4741)]: ex.append((P[k],sc))
json.dump(ex,open('extra.json','w'))
EOF
cat > sa3.py <<'EOF'
exec(open('search.py').read().split('for name,T')[0])
import random,math,sys
seed=int(sys.argv[1]);random.seed(seed)
obs+= [(S,sc) for S,sc in json.load(open('extra.json'))]
VS=[(wl(S),sc) for S,sc in obs]
TN=33.70
def l1(T):
    c=collections.Counter()
    for u in T:
        if u==s: c[('s',len(A[u]&T))]+=1
        else: c[(
```

```bash
cd /tmp/w; sed -e 's/bd=\[v for u in N for v in A\[u\] if v not in N\]/bd=[v for u in N for v in A[u] if v not in N and d[v]<=RR]/' -e 's/^T=set(json.load(open(sys.argv\[2\])))/RR=int(sys.argv[5]);T={x for x in json.load(open(sys.argv[2])) if d[x]<=RR}/' sa3.py > sa4.py
sed -i 's/if s not in N or not conn(N): continue/if s not in N or not conn(N): continue/' sa4.py
python3 -c "
import json;d=json.load(open('/tmp/w/g.json'))['dist'];json.dump([k for k in d if d[k]<=2],open('/tmp/w/b2.json','w'))"
for i in 1 2 3; do timeout 1500 python3 sa4.py $i b2.json 200 20000 4 & done; for i in 4 5 6; do ti
```

```bash
cd /tmp/w; cat > rules.py <<'EOF'
import json,collections,itertools
exec(open('wl.py').read())
def l1(T):
    c=collections.Counter()
    for u in T:
        if u==s: c[('s',len(A[u]&T))]+=1
        else: c[(len(A[u]&T), s in A[u]&T)]+=1
    return c
TGT=collections.Counter({('s',2):1,(2,False):6,(3,False):13,(4,False):7,(2,True):1,(3,True):1})
def dist(adj,src,r=99):
    D={src:0};q=[src]
    for u in q:
        if D[u]<r:
            for v in adj[u]:
                if v not in D: D[v]=D[u]+1;q.append(v)
    return D
found=[]
def chk(name,T):
    T=set(T)
    if len(T)==29: 
        diff=sum
```

```bash
cd /tmp/w; cat >> rules.py <<'EOF'
for D in itertools.chain.from_iterable(itertools.combinations(degs,k) for k in range(1,8)):
  for r in range(1,20):
    T=[x for x,v in d.items() if v<=r and (x==s or len(A[x]) in D)]
    chk(f'ball{r}deg{D}',T)
  for R in itertools.chain.from_iterable(itertools.combinations(range(1,12),k) for k in range(1,5)):
    T=[x for x,v in d.items() if v in R and len(A[x]) in D]+[s]
    chk(f'dists{R}deg{D}',T)
print('end2')
EOF
python3 rules.py 2>&1 | tail -20
```

```bash
cd /tmp/w; for i in 1 4 2; do echo -n "$i "; python3 -c "import json;print('\n'.join(json.load(open('b3_$i.json'))))" | probe evaluate -; done
```

```bash
cd /tmp/w; cat > deep.py <<'EOF'
import json,collections,numpy as np,sys
exec(open('wl.py').read())
TN=33.70
def wlfull(S,h=3):
    S=set(S);lab={u:('s' if u==s else 'x') for u in S};levels=[dict(lab)]
    for i in range(1,h+1):
        lab={u:(lab[u],tuple(sorted(lab[v] for v in A[u]&S))) for u in S}
        lab={u:hash(l) for u,l in lab.items()};levels.append(dict(lab))
    return levels
# T level0/1 counts as label->count using canonical
def l1lab(k,adj_s): pass
ex=json.load(open('extra.json'))
for S,sc in ex:
    if sc<0.9: continue
    v=wl(S);nrm=np.sqrt(sum(x*x for x in v.values()))
   
```

```bash
cd /tmp/w; sed -e 's/if s not in N or not conn(N): continue/if s not in N: continue/' -e 's/bd=\[v for u in N for v in A\[u\] if v not in N\]; N.add(random.choice(bd))/bd=[v for u in N for v in A[u] if v not in N]; N.add(random.choice(bd) if random.random()<0.7 else random.choice(POOL))/' -e 's/^TN=33.70/TN=33.704;POOL=[k for k in d if d[k]<=8]/' sa3.py > sa5.py; grep -n "POOL\|conn(N)" sa5.py; for i in 1 2 3 4 5 6; do timeout 1500 python3 sa5.py $i best14.json 300 25000 & done; wait
```

```bash
cd /tmp/w; python3 -c "
import json,collections
exec(open('wl.py').read())
T=set(json.load(open('b3_2.json')))
seen={s};q=[s]
for u in q:
  for v in A[u]&T:
    if v not in seen: seen.add(v);q.append(v)
print(len(seen),len(T),sorted(collections.Counter(d[x] for x in T).items()))
print('\n'.join(T),file=open('c','w'))"; probe evaluate - < c
```

```bash
cd /tmp/w; cat > rules2.py <<'EOF'
import json,collections,itertools
exec(open('rules.py').read().split('found=[]')[0])
sig={s:1}
order=sorted(d,key=d.get)
for u in order:
    if u!=s: sig[u]=sum(sig[p] for p in A[u] if d[p]==d[u]-1)
F={}
for u in d:
    F[u]={'deg':len(A[u]),'sig':sig[u],'par':sum(d[p]==d[u]-1 for p in A[u]),'sib':sum(d[p]==d[u] for p in A[u]),'ch':sum(d[p]==d[u]+1 for p in A[u]),
          'tri':sum(1 for x in A[u] for y in A[u] if x<y and y in A[x])}
best=[]
def score(T):
    h=l1(T);return sum(abs(h[k]-TGT[k]) for k in set(h)|set(TGT))
for r in range(1,15):
  for f in F[s]
```

```bash
cd /tmp/w; python3 -c "
import json,collections
exec(open('wl.py').read())
sets={n:set(json.load(open(n))) for n in ['b3_2.json','best14.json','best3.json','best11.json','best12.json','best2.json']}
cnt=collections.Counter(x for S in sets.values() for x in S)
for x,c in sorted(cnt.items(),key=lambda t:(d[t[0]],-t[1])): print(d[x],x,c,len(A[x]),[d[y] for y in A[x]])
" | head -60
```

```bash
probe neighbors 40234ca2ac; probe neighbors e6f6a117af; probe status
```

```bash
cd /tmp/w; python3 - <<'EOF'
exec(open('rules.py').read().split('found=[]')[0])
for r in [4,5,6]:
    T={u for u in d if d[u]<=r and len(A[u])==4}
    print(r,len(T),dict(l1(T)))
EOF
```

```bash
cd /tmp/w; python3 - <<'EOF'
exec(open('rules.py').read().split('found=[]')[0])
res=[]
for c in A:
    D=dist(A,c,8)
    for r in range(1,9):
        T={u for u in D if D[u]<=r}
        if s in T and 20<=len(T)<=40:
            h=l1(T);res.append((sum(abs(h[k]-TGT[k]) for k in set(h)|set(TGT)),len(T),c,r,d[c]))
res.sort();print(res[:10])
EOF
```

```bash
cd /tmp/w; python3 - <<'EOF'
exec(open('rules.py').read().split('found=[]')[0])
res=[]
Ds={r:{u for u in d if d[u]<=r} for r in range(1,12)}
for c in [k for k in d if d[k]<=8]:
    D=dist(A,c,10)
    for r in range(1,10):
        T0={u for u in D if D[u]<=r}
        if s not in T0: continue
        for r2 in range(2,11):
            T=T0&Ds[r2]
            if 25<=len(T)<=33:
                h=l1(T);res.append((sum(abs(h[k]-TGT[k]) for k in set(h)|set(TGT)),len(T),c,r,r2))
res.sort();print(res[:10])
EOF
```

```bash
nproc; cd /tmp/w; python3 - <<'EOF'
import json
ex=json.load(open('extra.json'))
for f,sc in [('b3_1.json',.9446),('b3_4.json',.9215),('b3_2.json',.9612)]:
    ex.append((json.load(open(f)),sc))
json.dump(ex,open('extra.json','w'))
EOF
cp b3_2.json seedA.json
```

```bash
cd /tmp/w; for i in $(seq 100 163); do st=seedA.json; [ $((i%2)) = 0 ] && st=best14.json; timeout 2400 python3 sa5.py $i $st $((100 + (i%4)*150)) 40000 > out_$i.txt 2>&1 & done; wait; cat out_1*.txt | sort -k2 -n | head
```

```bash
sleep 540; ls /tmp/w/out_1*.txt | wc -l; cat /tmp/w/out_1*.txt | sort -k2 -n | head -5
```

```bash
cd /tmp/w; timeout 100 python3 deep.py | tail -3
```

```bash
until [ $(ls /tmp/w/out_1*.txt 2>/dev/null | xargs -r cat | wc -l) -ge 64 ]; do sleep 10; done; cat /tmp/w/out_1*.txt | sort -k2 -n | head -8
```

```bash
until [ $(cat /tmp/w/out_1*.txt 2>/dev/null | wc -l) -ge 64 ]; do sleep 10; done; cat /tmp/w/out_1*.txt | sort -k2 -n | head -8
```

