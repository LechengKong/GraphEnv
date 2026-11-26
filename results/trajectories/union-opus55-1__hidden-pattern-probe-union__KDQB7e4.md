# union-opus55-1 / hidden-pattern-probe-union__KDQB7e4

model=bedrock/us.anthropic.claude-opus-5-5 reward=0.0 exception=AgentTimeoutError evaluate=85 best=0.9778

```bash
probe --help; probe status
```

**agent:** Let me explore the graph via BFS (free).

```bash
mkdir -p /tmp/w && cd /tmp/w && probe neighbors 5c37187f6d; cat > bfs.py <<'EOF'
import json,subprocess,collections
s="5c37187f6d"
adj={};dist={s:0};q=collections.deque([s])
while q:
    u=q.popleft()
    out=json.loads(subprocess.run(["probe","neighbors",u],capture_output=True,text=True).stdout)
    nb=out if isinstance(out,list) else out.get("neighbors",out)
    adj[u]=nb
    for v in nb:
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
json.dump({"adj":adj,"dist":dist},open("g.json","w"))
print(len(dist),collections.Counter(dist.values()))
EOF
python3 bfs.py
```

```bash
cd /tmp/w && python3 -c "
import json,collections
g=json.load(open('g.json'));adj=g['adj'];d=g['dist']
print(collections.Counter(len(v) for v in adj.values()))
asym=sum(1 for u in adj for v in adj[u] if u not in adj[v]);print('asym',asym)
for k in range(5): print(k,sum(1 for x in d.values() if x<=k))
"
for k in 0 1 2 3; do python3 -c "
import json;d=json.load(open('/tmp/w/g.json'))['dist'];print('\n'.join(x for x in d if d[x]<=$k))" | probe evaluate -; done
```

```bash
cd /tmp/w; for k in 4 5 6; do python3 -c "
import json;d=json.load(open('/tmp/w/g.json'))['dist'];print('\n'.join(x for x in d if d[x]<=$k))" | probe evaluate -; done
```

```bash
cd /tmp/w; python3 -c "
import json;d=json.load(open('g.json'))['dist']
for x in d:
  if d[x]==3: print(x)" > d3.txt
for x in $(cat d3.txt); do (python3 -c "
import json;d=json.load(open('/tmp/w/g.json'))['dist'];print('\n'.join(x for x in d if d[x]<=2))"; echo $x) | probe evaluate - | tr '\n' ' '; echo $x; done
```

```bash
cd /tmp/w; python3 -c "
import json;g=json.load(open('g.json'));adj=g['adj'];d=g['dist']
for x in d:
  if d[x]<=4: print(d[x],x,len(adj[x]),[ (y,d[y]) for y in adj[x]])"
```

```bash
cd /tmp/w; for x in 1486027e39 4e85239fbf 544f3d78bd ab5868ff09; do probe evaluate $x | tr '\n' ' '; echo $x; done; probe evaluate 5c37187f6d 4e85239fbf
```

```bash
cd /tmp/w; probe evaluate 1486027e39 4e85239fbf; probe evaluate 6f3564ba95; python3 -c "
import json;d=json.load(open('g.json'))['dist'];print(' '.join([x for x in d if d[x]==30][:5]))" > far5; probe evaluate $(head -c 10 far5); probe evaluate $(cat far5)
```

```bash
cd /tmp/w; probe evaluate 5c37187f6d; probe evaluate 5c37187f6d 1486027e39; probe evaluate 5c37187f6d 6f3564ba95
```

```bash
cd /tmp/w; F=($(cat far5)); probe evaluate ${F[0]} ${F[1]} ${F[2]}; probe evaluate 5c37187f6d ${F[0]} ${F[1]}; probe evaluate 5c37187f6d ${F[@]}; probe evaluate 1486027e39 4e85239fbf 544f3d78bd
```

```bash
cd /tmp/w; cat > ev.py <<'EOF'
import json,sys,subprocess
g=json.load(open('/tmp/w/g.json'));adj=g['adj'];d=g['dist']
def ev(S):
    S=list(dict.fromkeys(S))
    r=subprocess.run(["probe","evaluate","-"],input="\n".join(S),capture_output=True,text=True)
    return json.loads(r.stdout)["score"] if r.stdout else r.stderr
EOF
python3 -c "
exec(open('ev.py').read())
for k in [7,8]: S=[x for x in d if d[x]<=k]; print(k,len(S),ev(S))
for k in [1,2,3]: S=[x for x in d if d[x]==k]; print('shell',k,len(S),ev(S))
"
```

```bash
cd /tmp/w; F=($(cat far5)); probe evaluate ${F[0]} 5c37187f6d; probe evaluate ${F[0]} ${F[1]}; probe evaluate ${F[0]} ${F[3]};python3 -c "
exec(open('ev.py').read())
F=open('far5').read().split()
import itertools
for a,b in itertools.combinations(F,2): print(a,b,[y for y in adj[a] if y==b])
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('ev.py').read())
b3=[x for x in d if d[x]<=3]
print('b3-s',ev(b3[1:]))
b2=[x for x in d if d[x]<=2]
print('b2-s',ev(b2[1:]))
print('b2+ab+fc',ev(b2+['ab5868ff09','fcf8a911e7']))
"
```

```bash
cd /tmp/w; probe evaluate dfea12a08d fc6313d257; probe evaluate 1486027e39 68a3a1b9ad; probe evaluate 1486027e39 68a3a1b9ad 544f3d78bd; probe evaluate 1486027e39 68a3a1b9ad 544f3d78bd 5c37187f6d
```

```bash
cd /tmp/w; python3 -c "
exec(open('ev.py').read())
import collections
deg={u:len(adj[u]) for u in adj}
def comp(pred):
    s='5c37187f6d';seen={s};q=[s]
    while q:
        u=q.pop()
        for v in adj[u]:
            if v not in seen and pred(v): seen.add(v);q.append(v)
    return seen
for k in [2,3,4]:
    c=comp(lambda v:deg[v]<=k); print('deg<=',k,len(c))
    c=comp(lambda v:deg[v]==k); print('deg==',k,len(c))
    c=comp(lambda v:deg[v]>=k); print('deg>=',k,len(c))
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('ev.py').read())
import collections
def bfs(s):
    D={s:0};q=collections.deque([s])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in D: D[v]=D[u]+1;q.append(v)
    return D
F=open('far5').read().split()
for a in F:
    D=bfs(a);print(a,len(adj[a]),[D[b] for b in F])
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('ev.py').read())
import collections
def bfs(s):
    D={s:0};q=collections.deque([s])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in D: D[v]=D[u]+1;q.append(v)
    return D
D=bfs('dfea12a08d')
S=[x for x in D if D[x]<=3]; print(len(S),ev(S))
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('ev.py').read())
for k in [4,5,6,7]: S=[x for x in d if d[x]==k]; print('shell',k,len(S),ev(S))
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('ev.py').read())
deg={u:len(adj[u]) for u in adj}
for r in [3,4,5]:
  for name,p in [('>=3',lambda v:deg[v]>=3),('<=4',lambda v:deg[v]<=4)]:
    S=[x for x in d if d[x]<=r and p(x)]; print(r,name,len(S),ev(S))
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('ev.py').read())
a='dfea12a08d'; b=[y for y in adj[a]]; print(ev([b[0],a,b[1]]), ev([a]+b[:3]))
s='5c37187f6d'; print(ev([s]+adj[s]))
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('ev.py').read())
for k in [9,10]: S=[x for x in d if d[x]<=k]; print(k,len(S),ev(S))
"
```

**agent:** Found a strong lead: the scores fit a Weisfeiler–Lehman (h=3) graph-kernel cosine similarity where the start item has a special label. Let me verify by simulation.

```bash
cd /tmp/w; cat > wl.py <<'EOF'
import json,collections,math
g=json.load(open('/tmp/w/g.json'));adj=g['adj'];d=g['dist'];S0='5c37187f6d'
def feats(S,h=3):
    S=set(S);lab={v:('s' if v==S0 else 'o') for v in S}
    c=collections.Counter(lab.values())
    for i in range(h):
        lab={v:(lab[v],tuple(sorted(lab[u] for u in adj[v] if u in S))) for v in S}
        c.update(lab.values())
    return c
def cos(a,b):
    dot=sum(a[k]*b.get(k,0) for k in a)
    return dot/math.sqrt(sum(x*x for x in a.values())*sum(x*x for x in b.values()))
EOF
python3 -c "
exec(open('wl.py').read())
ball=lambda r:[x 
```

```bash
cd /tmp/w; cat > data.py <<'EOF'
exec(open('/tmp/w/wl.py').read())
s=S0
ball=lambda r:[x for x in d if d[x]<=r]
shell=lambda r:[x for x in d if d[x]==r]
F=open('/tmp/w/far5').read().split()
b2=ball(2)
Q=[]
for k,v in zip(range(11),[.0102,.392,.6509,.8758,.8673,.8682,.8857,.8815,.8747,.8696,.8693]): Q.append((ball(k),v))
d3=open('/tmp/w/d3.txt').read().split()
for x,v in zip(d3,[.6451,.6451,.6988,.6988,.6988,.8037,.8037,.72,.72,.72]): Q.append((b2+[x],v))
Q+= [(['1486027e39'],.4064),([s,'4e85239fbf'],.2945),(F,.508),(F[:3],.4977),([s]+F[:2],.368),([s]+F,.4953),
 (ball(3)[1:],.884),(b2[1:],.663)
```

```bash
cd /tmp/w; cat > sa.py <<'EOF'
exec(open('/tmp/w/data.py').read())
import random,sys
random.seed(int(sys.argv[1]))
pool=[x for x in d if d[x]<=7]
T=set(ball(4)); cur=err(T); best=(cur,set(T))
temp=0.02
for it in range(20000):
    x=random.choice(pool)
    if x==s: continue
    T2=set(T); T2^={x}
    e=err(T2)
    if e<cur or random.random()<math.exp((cur-e)/temp):
        T,cur=T2,e
        if e<best[0]: best=(e,set(T))
    temp*=0.9997
print(best[0],len(best[1]),sorted(d[x] for x in best[1]))
json.dump(sorted(best[1]),open('/tmp/w/best%s.json'%sys.argv[1],'w'))
EOF
for i in 1 2 3; do python3 
```

```bash
cd /tmp/w; sed -i 's/range(20000)/range(60000)/; s/temp\*=0.9997/temp*=0.9999/' sa.py; sed -i 's/^T=set(ball(4))/T=set(ball(4))|set(random.sample(shell(5),7))/' sa.py; for i in 4 5 6 7; do python3 sa.py $i & done; wait
```

```bash
cd /tmp/w; python3 -c "
exec(open('data.py').read())
T=json.load(open('best3.json')); ft=feats(T)
for i,(f,v) in enumerate(QF): print(i,len(Q[i][0]),v,round(cos(f,ft),4))
"
```

```bash
sleep 240; cat /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/b9acc3sdg.output
```

```bash
cd /tmp/w; python3 -c "
exec(open('data.py').read())
import itertools
res=[]
deg={u:len(adj[u]) for u in adj}
for r in range(3,8):
  B=ball(r)
  for k in range(1,8):
    for nm,p in [('>=',lambda x:deg[x]>=k),('<=',lambda x:deg[x]<=k),('==',lambda x:deg[x]==k),('!=',lambda x:deg[x]!=k)]:
      T=[x for x in B if p(x) or x==s]
      # also connected comp version
      seen={s};st=[s];Tset=set(T)
      while st:
        u=st.pop()
        for v in adj[u]:
          if v in Tset and v not in seen: seen.add(v);st.append(v)
      for nm2,TT in [('raw',T),('cc',list(seen))]:
        if 30<=len(TT)<=
```

```bash
until [ $(grep -c '^0\.' /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/b9acc3sdg.output) -ge 4 ]; do sleep 5; done; cat /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/b9acc3sdg.output
```

```bash
cat /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/b9acc3sdg.output
```

```bash
cd /tmp/w; timeout 110 bash -c 'until [ -f best7.json ] && [ -f best4.json ] && [ -f best5.json ] && [ -f best6.json ] && [ $(find best4.json -newer sa.py | wc -l) -ge 1 ]; do sleep 3; done'; cat /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/b9acc3sdg.output
```

```bash
cd /tmp/w; cat > sa2.py <<'EOF'
exec(open('/tmp/w/data.py').read())
import random,sys
random.seed(int(sys.argv[1])); R=int(sys.argv[2])
pool=[x for x in d if d[x]<=R and x!=s]
T=set([s]+random.sample(pool,40)); cur=err(T); best=(cur,set(T))
temp=0.03
for it in range(40000):
    a=random.choice(list(T-{s}))
    # prefer neighbor-of-T additions
    cand=[v for u in T for v in adj[u] if v not in T and v in d and d[v]<=R]
    b=random.choice(cand) if random.random()<0.8 else random.choice(pool)
    if b in T: continue
    T2=set(T); T2.remove(a); T2.add(b)
    e=err(T2)
    if e<cur or random.rand
```

```bash
cd /tmp/w; python3 -c "
exec(open('data.py').read())
# candidate rules of size 41 containing s: nearest-41 by BFS order? check ties
import collections
print(collections.Counter(d[x] for x in d if d[x]<=5))
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('data.py').read())
for x in shell(5): print(x,deg[x],sum(1 for y in adj[x] if d[y]==4),sum(1 for y in adj[x] if d[y]==5))
" ; python3 -c "
exec(open('/tmp/w/data.py').read())
B4=ball(4)
for k in [1,2]:
  T=B4+[x for x in shell(5) if sum(1 for y in adj[x] if d[y]==4)>=k+0]
" 
```

```bash
cd /tmp/w; timeout 590 bash -c 'until [ $(ls b41_*.json 2>/dev/null | wc -l) -ge 4 ]; do sleep 5; done'; cat /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/bo1td4cao.output
```

```bash
cd /tmp/w; python3 -c "
exec(open('data.py').read())
import collections
for f in ['b41_4.json','b41_1.json']:
  T=set(json.load(open(f)))
  print(collections.Counter(sum(1 for y in adj[x] if y in T) for x in T if x!=s), sum(1 for y in adj[s] if y in T))
  ft=feats(T)
  print([ (i,v,round(cos(QF[i][0],ft),4)) for i in range(len(QF)) if abs(cos(QF[i][0],ft)-v)>0.002])
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('data.py').read())
for f in ['b41_4.json','b41_1.json','b41_2.json','b41_3.json']:
  T=set(json.load(open(f)))
  ft=feats(T)
  print(f,[y for y in adj[s] if y in T],[ (i,vv,round(cos(QF[i][0],ft),4)) for i,(ff,vv) in enumerate(QF) if abs(cos(ff,ft)-vv)>0.002])
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('data.py').read())
import collections
for k in [3,4]:
 for mode in ['>=','<=']:
  ok=lambda v:(deg[v]>=k if mode=='>=' else deg[v]<=k) or v==s
  D={s:0};q=collections.deque([s])
  while q:
    u=q.popleft()
    for v in adj[u]:
      if ok(v) and v not in D: D[v]=D[u]+1;q.append(v)
  for r in range(2,9):
    T=[x for x in D if D[x]<=r]
    print(k,mode,r,len(T),round(err(T),4))
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('data.py').read())
import collections
def core(T,k):
  T=set(T)
  while True:
    rm=[x for x in T if sum(1 for y in adj[x] if y in T)<k]
    if not rm: return T
    T-=set(rm)
def hist(T): return sorted(collections.Counter(sum(1 for y in adj[x] if y in T) for x in T).items())
for r in range(3,9):
  T=core(ball(r),2); print(r,len(T),s in T,round(err(T),4),hist(T))
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('data.py').read())
a='dfea12a08d'; b=adj[a]; print(b,[[y for y in adj[x] if y in b] for x in b])
"
```

```bash
cd /tmp/w; cat > iv.py <<'EOF'
exec(open('/tmp/w/data.py').read())
import collections
def bfs(a):
    D={a:0};q=collections.deque([a])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in D: D[v]=D[u]+1;q.append(v)
    return D
res=[]
for t in d:
    Dt=bfs(t); T=[v for v in d if d[v]+Dt[v]==d[t]]
    if 30<=len(T)<=55: res.append((err(T),t,len(T),d[t]))
res.sort(); print(res[:5])
EOF
python3 iv.py
```

```bash
cd /tmp/w; probe status; python3 -c "
exec(open('data.py').read())
import itertools
def indep_star(k):
  for c in d:
    if d[c]>15 and len(adj[c])>=k:
      for comb in itertools.combinations(adj[c],k):
        if all(b not in adj[a] for a,b in itertools.combinations(comb,2)): return [c]+list(comb)
for k in [4,5]:
  S=indep_star(k); print(k,S,ev(S))
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('data.py').read()); exec(open('ev.py').read())
import itertools
def indep_star(k):
  for c in d:
    if d[c]>15 and len(adj[c])>=k:
      for comb in itertools.combinations(adj[c],k):
        if all(b not in adj[a] for a,b in itertools.combinations(comb,2)): return [c]+list(comb)
for k in [2,4,5]:
  S=indep_star(k); print(k,S,ev(S))
" | tee -a log.txt
```

```bash
cd /tmp/w; cat > iv2.py <<'EOF'
exec(open('/tmp/w/data.py').read())
import collections
def bfs(a):
    D={a:0};q=collections.deque([a])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in D: D[v]=D[u]+1;q.append(v)
    return D
def sig(T):
    T=set(T); sn=set(adj[s])
    h=collections.Counter(sum(1 for y in adj[x] if y in T) for x in T if x!=s and x not in sn)
    return len(T), sum(1 for y in adj[s] if y in T), dict(h)
res=[]
for t in d:
    Dt=bfs(t)
    for k in range(0,4):
        T=[v for v in d if d[v]+Dt[v]<=d[t]+k]
        if 38<=len(T)<=44: res.append(
```

```bash
cd /tmp/w; cat > cyc.py <<'EOF'
exec(open('/tmp/w/iv2.py').read().split('res=[]')[0])
import sys
Lmax=int(sys.argv[1])
cover={}  # minimal cycle length per node
def dfs(path,vis):
    u=path[-1]
    if len(path)>Lmax: return
    for v in adj[u]:
        if v==s and len(path)>=3:
            L=len(path)
            for x in path: cover[x]=min(cover.get(x,99),L)
        elif v not in vis and d[v]<=Lmax//2+1:
            vis.add(v);path.append(v);dfs(path,vis);path.pop();vis.remove(v)
dfs([s],{s})
for L in range(3,Lmax+1):
    T=[x for x in cover if cover[x]<=L]
    print(L,len(T),round(err(T),4)
```

```bash
cd /tmp/w; cat >> log.txt <<'EOF'
K14 ['75d3fdf010', '309c906b6a', '89d5dd46a8', 'd1a81d9042', 'ea437de91d'] 0.4755
K15 ['53b5712812', '24675017e7', '2752162afa', '9da9485d68', 'ae582397f9', 'ecf0a39c9e'] 0.4567
EOF
python3 -c "
exec(open('iv2.py').read().split('res=[]')[0])
for t in ['ffec7db88d','63e72f7c1e','e29478d14f']:
  Dt=bfs(t); T=[v for v in d if d[v]+Dt[v]==d[t]]
  print(t,d[t],[x for x in adj[s] if x in T], sorted(collections.Counter(d[v] for v in T).items()))
"
```

```bash
cd /tmp/w; cat > sa3.py <<'EOF'
exec(open('/tmp/w/iv2.py').read().split('res=[]')[0])
import random,sys
for line in open('/tmp/w/log.txt'):
    p=line.split('['); 
    if len(p)<2: continue
    S=eval('['+p[1].split(']')[0]+']'); v=float(line.split(']')[-1])
    Q.append((S,v)); QF.append((feats(S),v))
def E(T):
    ft=feats(T); return sum((cos(f,ft)-v)**2 for f,v in QF)
random.seed(int(sys.argv[1]))
Dt=bfs(sys.argv[2]); T=set(v for v in d if d[v]+Dt[v]==d[sys.argv[2]])|set(adj[s])
while len(T)<41:
    T.add(random.choice([v for u in T for v in adj[u] if v not in T]))
cur=E(T);best=(cur,set(T)
```

```bash
cd /tmp/w; timeout 590 bash -c 'until [ $(ls sa3_*.json 2>/dev/null | wc -l) -ge 4 ]; do sleep 5; done'; cat /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/b7sm71aq4.output
```

```bash
cd /tmp/w; cat > lb.py <<'EOF'
exec(open('/tmp/w/sa3.py').read().split('def E(T)')[0])
N=49.21
def lb(S):
    S=set(S); f=feats(S)
    t={'s':1,'o':40,('s',('o','o','o')):1,('o',('o','o')):19,('o',('o','o','o')):14,('o',('o','o','o','o')):4,('o',('o','s')):1}
    dot=sum(f[k]*t.get(k,0) for k in f)
    return dot/(N*math.sqrt(sum(x*x for x in f.values())))
for (S,v),(f,_) in zip(Q,QF):
    print(len(S),v,round(lb(S),4), 'VIOL' if lb(S)>v+1e-3 else '')
EOF
python3 lb.py
```

```bash
cd /tmp/w; cat >> lb.py <<'EOF'
print('---')
for i,((S,v),(f,_)) in enumerate(zip(Q,QF)):
    nf=math.sqrt(sum(x*x for x in f.values()))
    r=(v-lb(S))*N*nf
    if abs(r)>0.3: print(i,len(S),round(r,2),'+-',round(0.00005*N*nf,2))
EOF
python3 lb.py | sed -n '/---/,$p'
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
import itertools
sh={k:shell(k) for k in range(0,12)}
res=[]
for r in range(1,7):
  for K in itertools.combinations(range(2,12),r):
    K=(0,1)+K
    if sum(len(sh[k]) for k in K)==41:
      T=[x for k in K for x in sh[k]]; res.append((round(err(T),4),K,sig(T)))
res.sort(); print(*res[:5],sep='\n')
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
res=[]
for t in d:
  Dt=bfs(t); I=set(v for v in d if d[v]+Dt[v]==d[t])
  T=I|set(adj[s])
  T2=T|{'68a3a1b9ad'}
  for nm,X in [('I+n',T),('I+n+68',T2)]:
    if 39<=len(X)<=43: res.append((round(err(X),4),t,nm,sig(X)))
res.sort(); print(*res[:6],sep='\n')
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
for f in ['sa3_1.json','sa3_4.json']:
  T=set(json.load(open(f))); ft=feats(T)
  print([x for x in adj[s] if x in T], sorted(collections.Counter(d[x] for x in T).items()))
  print([(i,v,round(cos(ff,ft),4)) for i,(ff,v) in enumerate(QF) if abs(cos(ff,ft)-v)>0.002])
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('data.py').read())
tri=sum(1 for u in adj for v in adj[u] for w in adj[v] if w in adj[u])//6
E=sum(len(v) for v in adj.values())//2
print('nodes',len(adj),'edges',E,'tri',tri)
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
import itertools
want={2:19,3:14,4:4}
hits=[]
for r in range(1,8):
  for m in range(1,7):
    for D in itertools.combinations([1,2,3,4,5,6,7],m):
      ok=lambda v:deg[v] in D or v==s
      DD={s:0};q=collections.deque([s])
      while q:
        u=q.popleft()
        for v in adj[u]:
          if ok(v) and v not in DD: DD[v]=DD[u]+1;q.append(v)
      T=[x for x in DD if DD[x]<=r]
      for TT in [T, [x for x in d if d[x]<=r and ok(x)]]:
        if len(TT)==41: hits.append((round(err(TT),4),r,D,sig(TT)))
hits.sort(); prin
```

```bash
cd /tmp/w; cat > lab.py <<'EOF'
exec(open('/tmp/w/sa3.py').read().split('def E(T)')[0])
names={}
def nm(l):
    if l not in names: names[l]='L%d'%len(names)
    return names[l]
def nodelabels(S,h=3):
    S=set(S);lab={v:('s' if v==S0 else 'o') for v in S}; out={v:[lab[v]] for v in S}
    for i in range(h):
        lab={v:(lab[v],tuple(sorted(lab[u] for u in adj[v] if u in S))) for v in S}
        for v in S: out[v].append(lab[v])
    return out
EOF
python3 -c "
exec(open('lab.py').read())
b2=ball(2)
for S in [b2, b2+['6ce4ea8b87'], b2+['57229fd2af'], b2+['ab5868ff09']]:
  L=nodelabels(S)
  pri
```

```bash
cd /tmp/w; cat > sa4.py <<'EOF'
exec(open('/tmp/w/sa3.py').read().split('def E(T)')[0])
import random,sys
want={2:19,3:14,4:4}
def E(T):
    ft=feats(T)
    e=sum((cos(f,ft)-v)**2 for f,v in QF)*100
    sn=set(adj[s])
    h=collections.Counter(sum(1 for y in adj[x] if y in T) for x in T if x!=s and x not in sn)
    e+=0.01*sum((h.get(k,0)-want.get(k,0))**2 for k in set(h)|set(want))
    e+=0.05*(3-sum(1 for y in adj[s] if y in T))**2 + 0.02*(len(T)-41)**2
    return e
random.seed(int(sys.argv[1]))
T=set(ball(1))|{'68a3a1b9ad'}
while len(T)<41: T.add(random.choice([v for u in T for v in adj[u] 
```

```bash
cd /tmp/w; timeout 590 bash -c 'until [ $(ls sa4_*.json 2>/dev/null | wc -l) -ge 8 ]; do sleep 5; done'; cat /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/b9gqrq254.output
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
for i in [8,3,6]:
  T=set(json.load(open('sa4_%d.json'%i)))
  print(i,sorted(collections.Counter(d[x] for x in T).items()), {k:len([x for x in d if d[x]==k]) for k in range(9)})
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
for r in [3,4,5]: print(r,sig(ball(r)))
"
```

```bash
cd /tmp/w; cat > fam.py <<'EOF'
exec(open('/tmp/w/sa3.py').read().split('def E(T)')[0])
want=(41,3,{2:19,3:14,4:4})
def gbfs(okedge):
    D={s:0};q=collections.deque([s])
    while q:
        u=q.popleft()
        for v in adj[u]:
            if v not in D and okedge(u,v): D[v]=D[u]+1;q.append(v)
    return D
fams={
 'deg_nonincr':lambda u,v:deg[v]<=deg[u],
 'deg_nondecr':lambda u,v:deg[v]>=deg[u],
 'deg_diff1':lambda u,v:abs(deg[v]-deg[u])<=1,
 'deg_ne':lambda u,v:deg[v]!=deg[u],
 'deg_eq_or_lower':lambda u,v:deg[v]<deg[u],
 'id_incr':lambda u,v:v>u,
 'id_decr':lambda u,v:v<u,
 'tri_edge':lam
```

```bash
cd /tmp/w; for i in 8 3 6 2; do v=$(probe evaluate - < <(python3 -c "import json;print('\n'.join(json.load(open('/tmp/w/sa4_$i.json'))))") | python3 -c "import json,sys;print(json.load(sys.stdin)['score'])"); echo "sa4_$i $(python3 -c "import json;print(json.load(open('/tmp/w/sa4_$i.json')))") $v" >> log.txt; echo $i $v; done
```

```bash
cd /tmp/w; sed -i 's/^T=set(ball(1))|{.68a3a1b9ad.}/T=set(json.load(open(sys.argv[4]))) if len(sys.argv)>4 else set(ball(1))|{"68a3a1b9ad"}/' sa4.py; grep -n "^T=" sa4.py; for i in 11 12 13 14; do python3 sa4.py $i 30000 0.03 sa4_8.json & done; for i in 15 16 17 18; do python3 sa4.py $i 30000 0.03 sa4_3.json & done; wait
```

```bash
cd /tmp/w; timeout 590 bash -c 'until [ $(grep -c "^[0-9]" /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/bmev8gzys.output) -ge 8 ]; do sleep 5; done'; cat /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/bmev8gzys.output | grep '^[0-9]'
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
A=[set(json.load(open('sa4_%d.json'%i))) for i in [8,3,6,2]]
I=set.intersection(*A); U=set.union(*A)
print(len(I),len(U))
print(sorted((d[x],x[:4],deg[x]) for x in I))
B3=set(ball(3)); print('ball3 not in I',[(x[:4],deg[x]) for x in B3-I])
"
```

```bash
cd /tmp/w; cat > fam2.py <<'EOF'
exec(open('/tmp/w/sa3.py').read().split('def E(T)')[0])
want={2:19,3:14,4:4}
def good(T):
    g=sig(T); return g[0]==41 and g[1]==3
cands=[]
# family 4-6
for r in range(3,9):
    B=set(ball(r))
    for k in range(1,5):
        T=[x for x in B if sum(1 for y in adj[x] if y in B)>=k or x==s]; cands.append(('nbrsinball>=%d r%d'%(k,r),T))
        T=[x for x in B if sum(1 for y in adj[x] if d[y]==d[x]-1)>=k or x==s]; cands.append(('parents>=%d r%d'%(k,r),T))
        T=[x for x in B if sum(1 for y in adj[x] if d[y]==d[x])>=k or x==s]; cands.append(('samelvl>=%d r%d'%
```

```bash
cd /tmp/w; cat > fam3.py <<'EOF'
exec(open('/tmp/w/sa3.py').read().split('def E(T)')[0])
want={2:19,3:14,4:4}
near=[x for x in d if d[x]<=12]
hits=[]
for t in near:
    Dt=bfs(t)
    for r1 in range(2,10):
        for r2 in range(1,14):
            T=[v for v in d if d[v]<=r1 and Dt[v]<=r2]
            if len(T)!=41 or s not in T: continue
            g=sig(T)
            if g[1]==3: hits.append((round(err(T),4),t,r1,r2,g))
            # also union
hits.sort(); print(len(hits)); print(*hits[:8],sep='\n')
EOF
python3 fam3.py
```

```bash
cd /tmp/w; cat > sa5.py <<'EOF'
exec(open('/tmp/w/sa3.py').read().split('def E(T)')[0])
import random,sys
def E(T):
    if s not in T: return 9
    ft=feats(T); return sum((cos(f,ft)-v)**2 for f,v in QF)*100
random.seed(int(sys.argv[1]))
T=set(json.load(open(sys.argv[4])))
cur=E(T);best=(cur,set(T));temp=float(sys.argv[3])
for it in range(int(sys.argv[2])):
    r=random.random()
    T2=set(T)
    if r<0.5: T2.discard(random.choice(list(T-{s})))
    if r>0.25:
        if random.random()<0.9: T2.add(random.choice([v for u in T for v in adj[u] if v not in T]))
        else: T2.add(random.choice(l
```

```bash
cd /tmp/w; timeout 590 bash -c 'until [ $(ls sa5_*.json 2>/dev/null | wc -l) -ge 8 ]; do sleep 5; done'; grep '^[0-9]' /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/bi6sbagg6.output
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
intri={u:any(w in adj[u] for v in adj[u] for w in adj[v]) for u in adj}
print('s in tri',intri[s],[intri[x] for x in adj[s]], sum(intri.values()))
for flag in [True,False]:
  ok=lambda v:intri[v]==flag or v==s
  DD={s:0};q=collections.deque([s])
  while q:
    u=q.popleft()
    for v in adj[u]:
      if ok(v) and v not in DD: DD[v]=DD[u]+1;q.append(v)
  print(flag,len(DD))
  for r in range(2,12):
    T=[x for x in DD if DD[x]<=r]; print(r,len(T),sig(T),round(err(T),4))
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
order=sorted(d,key=lambda x:d[x]); sig_={s:1}
for v in order[1:]: sig_[v]=sum(sig_[u] for u in adj[v] if d[u]==d[v]-1)
for r in range(3,12):
  for k in [1,2,3,4]:
    T=[x for x in d if d[x]<=r and (sig_[x]<=k or x==s)]
    T2=[x for x in d if d[x]<=r and (sig_[x]>=k or d[x]<=1)]
    for nm,TT in [('<=',T),('>=',T2)]:
      if 36<=len(TT)<=46: print(r,nm,k,len(TT),sig(TT),round(err(TT),4))
"
```

```bash
cd /tmp/w; cat > evf.sh <<'EOF'
#!/bin/bash
# usage: evf.sh name.json
f=$1
v=$(python3 -c "import json;print('\n'.join(json.load(open('/tmp/w/$f'))))" | probe evaluate - | python3 -c "import json,sys;print(json.load(sys.stdin)['score'])")
echo "$f $(python3 -c "import json;print(json.load(open('/tmp/w/$f')))") $v" >> /tmp/w/log.txt
echo $f $v
EOF
chmod +x evf.sh; for f in sa5_8.json sa5_4.json sa5_1.json sa5_5.json; do ./evf.sh $f; done
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
T=set(json.load(open('sa5_1.json')))
for x in sorted(T,key=lambda x:d[x]): print(d[x],x[:6],deg[x],sum(1 for y in adj[x] if y in T),[ (y[:4],d[y]) for y in adj[x] if y in T])
"
```

```bash
cd /tmp/w; cat > fam4.py <<'EOF'
exec(open('/tmp/w/sa3.py').read().split('def E(T)')[0])
import itertools
def core(T,k=2):
  T=set(T)
  while True:
    rm=[x for x in T if sum(1 for y in adj[x] if y in T)<k]
    if not rm: return T
    T-=set(rm)
def comp(T):
  if s not in T: return set()
  seen={s};st=[s]
  while st:
    u=st.pop()
    for v in adj[u]:
      if v in T and v not in seen: seen.add(v);st.append(v)
  return seen
bases=[]
for r in range(2,10):
  B=ball(r); bases.append(('ball%d'%r,B))
  for m in range(1,6):
    for D in itertools.combinations([2,3,4,5,6,7],m):
      bases.append((
```

```bash
cd /tmp/w; for i in 21 22 23 24; do python3 sa5.py $i 40000 0.01 sa5_1.json & done; for i in 25 26 27 28; do python3 sa5.py $i 40000 0.01 sa5_5.json & done; wait; grep -h . /dev/null
```

```bash
cd /tmp/w; timeout 595 bash -c 'until [ $(grep -c "^[0-9]" /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/b9lha1lcv.output) -ge 8 ]; do sleep 5; done'; grep '^[0-9]' /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/b9lha1lcv.output
```

```bash
cd /tmp/w; python3 -c "
exec(open('ev.py').read())
import math
for S in [['5c37187f6d','1486027e39','68a3a1b9ad','f39000d409'],['5c37187f6d','4e85239fbf','0b09234e84','d90ecca08a','e7078ff91d']]:
  v=ev(S); print(S,v)
  open('/tmp/w/log.txt','a').write('q %s %s\n'%(S,v))
"
```

```bash
cd /tmp/w; cat > lb2.py <<'EOF'
exec(open('/tmp/w/sa3.py').read().split('def E(T)')[0])
N=math.sqrt(1601+ (1+361+196+16+1+1+1) + 248)
t1={'s':1,'o':40,('s',('o','o','o')):1,('o',('o','o')):19,('o',('o','o','o')):14,('o',('o','o','o','o')):4,('o',('o','s')):1,('o',('o','o','s')):1,('o',('o','o','o','s')):1}
def res(S,v):
    f=feats(S); nf=math.sqrt(sum(x*x for x in f.values()))
    return v*N*nf - sum(f[k]*t1.get(k,0) for k in f), 0.00005*N*nf
if __name__=='__main__':
  for i,(S,v) in enumerate(Q):
    r,e=res(S,v); print(i,len(S),v,round(r,2),'+-',round(e,2))
EOF
python3 lb2.py
```

```bash
cd /tmp/w; sed -i 's/^N=math.sqrt.*/N=49.21/' lb2.py; python3 lb2.py | awk '{print $0}' | tr '\n' ';'
```

```bash
cd /tmp/w; cat > sa6.py <<'EOF'
exec(open('/tmp/w/sa3.py').read().split('def E(T)')[0])
import random,sys
want={2:19,3:14,4:4}
B2=set(ball(2))
def E(T):
    ft=feats(T)
    e=sum((cos(f,ft)-v)**2 for f,v in QF)*1000
    sn=set(adj[s])
    h=collections.Counter(sum(1 for y in adj[x] if y in T) for x in T if x!=s and x not in sn)
    e+=0.3*sum(abs(h.get(k,0)-want.get(k,0)) for k in set(h)|set(want))
    return e
random.seed(int(sys.argv[1]))
if len(sys.argv)>4:
    T=set(json.load(open(sys.argv[4])))|B2
    while len(T)>41: T.discard(random.choice(list(T-B2)))
else: T=set(B2)
while len(T)<41: T
```

```bash
cd /tmp/w; timeout 595 bash -c 'until [ $(grep -c "^[0-9]" /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/b23019uww.output) -ge 8 ]; do sleep 5; done'; grep '^[0-9]' /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/b23019uww.output
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
res=[]
for t in d:
  Dt=bfs(t)
  for k in [0,1]:
    T=[v for v in d if d[v]+Dt[v]<=d[t]+k]
    g=sig(T)
    if g[1]==3 and len(T)<=80: res.append((round(err(T),4),t,k,d[t],g))
res.sort(); print(len(res)); print(*res[:8],sep='\n')
"
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
A=[set(json.load(open('sa6_%d.json'%i))) for i in range(1,9)]
for x in shell(3)+shell(4):
  print(d[x],x[:4],deg[x],''.join('1' if x in a else '.' for a in A))
"
```

```bash
cd /tmp/w; cat > q.py <<'EOF'
import sys
exec(open('/tmp/w/lb2.py').read().split("if __name__")[0])
exec(open('/tmp/w/ev.py').read())
S=sys.argv[1].split(',')
S=[x for x in d if any(x.startswith(p) for p in S)] if all(len(p)<10 for p in S) else S
v=ev(S); r,e=res(S,v)
open('/tmp/w/log.txt','a').write('q %s %s\n'%(S,v))
print(v, round(r,2),'+-',round(e,2))
EOF
B2=5c37,1486,4e85,544f,68a3,f390,0b09,d90e,e707
python3 q.py $B2,ce23,5722; python3 q.py $B2,ce23,5722,6930
```

```bash
cd /tmp/w; B=5c37,1486,4e85,544f,68a3,f390,0b09,d90e,e707,ce23,5722; python3 q.py $B,ab58,fcf8,c92f; python3 q.py $B,ab58,fcf8,c92f,4d4e
```

```bash
cd /tmp/w; sed -i 's/^B2=set(ball(2))/B2=set(ball(2))|{"ce23e6afce"}/' sa6.py; for i in 11 12 13 14; do python3 sa6.py $i 30000 1.0 sa6_8.json & done; for i in 15 16 17 18; do python3 sa6.py $i 30000 1.0 sa6_5.json & done; wait
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
far=[x for x in d if d[x]==49]
U=set()
for t in far:
  Dt=bfs(t); I=[v for v in d if d[v]+Dt[v]==49]; U|=set(I); print(t,len(I),sig(I))
print(len(U))
"
```

```bash
cd /tmp/w; timeout 595 bash -c 'until [ $(grep -c "^[0-9]" /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/b2uu34v1o.output) -ge 8 ]; do sleep 5; done'; grep '^[0-9]' /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/b2uu34v1o.output
```

```bash
cd /tmp/w; python3 -c "
exec(open('sa3.py').read().split('def E(T)')[0])
B2=set(ball(2))|{'ce23e6afce'}
res=[]
for t in d:
  Dt=bfs(t)
  for k in range(0,8):
    T=[v for v in d if d[v]+Dt[v]<=d[t]+k]
    if len(T)>60: break
    if len(T)==41 and B2<=set(T): res.append((round(err(T),4),t,k,sig(T)))
res.sort(); print(len(res)); print(*res[:8],sep='\n')
"
```

```bash
cd /tmp/w; P=5c37,1486,4e85,544f,68a3,f390,0b09,d90e,e707,ce23,5722,ab58,fcf8,c92f; python3 q.py $P,0131; python3 q.py $P,0131,71e8
```

```bash
cd /tmp/w; sed -i 's/^B2=set(ball(2)).*/B2=set(ball(2))|{"ce23e6afce","013152936d","71e8cf11ba"}; OUT={"6ce4ea8b87","6f3564ba95"}/' sa6.py; sed -i 's/    b=random.choice(\[v for u in T for v in adj\[u\] if v not in T\])/    b=random.choice([v for u in T for v in adj[u] if v not in T and v not in OUT])/' sa6.py; grep -n "OUT" sa6.py; for i in 31 32 33 34 35 36 37 38; do python3 sa6.py $i 30000 2.0 & done; wait
```

```bash
cd /tmp/w; P2=5c37,1486,4e85,544f,68a3,f390,0b09,d90e,e707,ce23,5722,ab58,fcf8,c92f,0131,71e8; python3 q.py $P2,cd50; python3 q.py $P2,cd50,f8c5
```

```bash
cd /tmp/w; timeout 595 bash -c 'until [ $(grep -c "^[0-9]" /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/bj8ib5mgi.output) -ge 8 ]; do sleep 5; done'; grep '^[0-9]' /tmp/claude-0/-app/ca4f3926-f368-4e22-89d0-63729c32e024/tasks/bj8ib5mgi.output; python3 -c "
exec(open('/tmp/w/sa3.py').read().split('def E(T)')[0])
A=[set(json.load(open('/tmp/w/sa6_%d.json'%i))) for i in range(31,39)]
for x in sorted(set.union(*A),key=lambda x:d[x]):
  print(d[x],x[:4],deg[x],''.join('1' if x in a else '.' for a in A))
"
```

```bash
nproc; cd /tmp/w; wc -l log.txt; tail -3 log.txt | cut -c1-80
```

```bash
cd /tmp/w; for i in $(seq 100 163); do python3 sa6.py $i 40000 2.0 sa6_3$((i%8+1)).json > out_$i.txt & done; wait; sort -g out_1*.txt | head -5
```

```bash
cd /tmp/w; timeout 595 bash -c 'until [ $(cat out_1*.txt | grep -c "^[0-9]") -ge 64 ]; do sleep 5; done'; sort -g out_1*.txt | head -5
```

