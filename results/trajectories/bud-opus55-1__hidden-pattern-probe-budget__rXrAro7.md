# bud-opus55-1 / hidden-pattern-probe-budget__rXrAro7

model=bedrock/us.anthropic.claude-opus-5-5 reward=0.0 exception=AgentTimeoutError evaluate=125 best=0.9538

```bash
probe --help; probe status
```

```bash
probe neighbors 333671762b; probe evaluate 333671762b
```

```bash
cd /tmp; cat > bfs.py <<'EOF'
import json,subprocess,sys
start="333671762b"
adj={}
def nb(x):
    if x not in adj:
        adj[x]=json.loads(subprocess.check_output(["probe","neighbors",x]))["neighbors"]
    return adj[x]
dist={start:0};front=[start]
for d in range(1,int(sys.argv[1])+1):
    nf=[]
    for u in front:
        for v in nb(u):
            if v not in dist: dist[v]=d; nf.append(v)
    front=nf
    print(d,len(nf),sum(1 for v in dist))
json.dump({"adj":adj,"dist":dist},open("g.json","w"))
EOF
python3 bfs.py 3
```

```bash
cd /tmp; python3 -c "
import json;g=json.load(open('g.json'))
for k,v in g['adj'].items(): print(k,g['dist'][k],len(v),v)
"; python3 -c "
import json,subprocess;g=json.load(open('/tmp/g.json'))
for r in [1,2,3]:
  s=[k for k,d in g['dist'].items() if d<=r]
  print(r,len(s),subprocess.check_output(['probe','evaluate']+s).decode())
"
```

```bash
cd /tmp; python3 bfs.py 5; python3 -c "
import json,subprocess;g=json.load(open('/tmp/g.json'))
for r in [4,5]:
  s=[k for k,d in g['dist'].items() if d<=r]
  print(r,len(s),subprocess.check_output(['probe','evaluate']+s).decode())
"
```

**agent:** Ball scores so far: radius 3 → 0.85, 4 → 0.917, 5 → 0.929. Not a clean ball yet; expanding further.

```bash
cd /tmp; python3 bfs.py 7; python3 -c "
import json,subprocess;g=json.load(open('/tmp/g.json'))
for r in [6,7]:
  s=[k for k,d in g['dist'].items() if d<=r]
  if len(s)<=200: print(r,len(s),subprocess.check_output(['probe','evaluate']+s).decode())
"; probe status
```

```bash
cd /tmp; python3 -c "
import json;g=json.load(open('g.json'));adj=g['adj'];dist=g['dist']
from collections import Counter
for d in range(7):
  print(d,sorted(Counter(len(adj[k]) for k,dd in dist.items() if dd==d).items()))
"
```

```bash
cd /tmp; python3 -c "
import json,subprocess;g=json.load(open('/tmp/g.json'));dist=g['dist']
b4=[k for k,d in dist.items() if d<=4]
def ev(s): return json.loads(subprocess.check_output(['probe','evaluate']+s))['score']
for k,d in dist.items():
  if d==5: print('add',k,ev(b4+[k]))
  if d==4: print('rem',k,ev([x for x in b4 if x!=k]))
"
```

**agent:** Marginal tests show the score isn't plain Jaccard over a ball — some radius-4 items hurt and some radius-5 items help. Switching to greedy flips.

```bash
cd /tmp; cat > ls.py <<'EOF'
import json,subprocess,sys
g=json.load(open('/tmp/g.json'));dist=g['dist']
def ev(s): return json.loads(subprocess.check_output(['probe','evaluate']+sorted(s)))['score']
S=set(json.load(open(sys.argv[1])))
cands=json.load(open(sys.argv[2]))
base=ev(S);print('base',base)
for k in cands:
    T=S^{k}
    sc=ev(T)
    if sc>base: S=T;base=sc;print('flip',k,dist[k],k in S,sc,flush=True)
    if base>=1: break
json.dump(sorted(S),open('/tmp/S.json','w'));print(base,len(S))
EOF
python3 -c "
import json;g=json.load(open('/tmp/g.json'));d=g['dist']
json.dump([k for k,v in d.
```

```bash
cd /tmp; python3 -c "
import json,subprocess;g=json.load(open('/tmp/g.json'));d=g['dist']
S=set(k for k,v in d.items() if v<=4)
S-= {'7f1652550c','41e5de6445','c08448f987','f489ee9e06','0255797ca1','7db0ec9ab4','32049e6a41','ed74ad5368','8e67360323'}
S|={'715cfb33ce','521e5d33f6','69ab4ee267','71543b6fa1','0238aaa06c','b0aaf331c9','10e8d65088','447e4b8f34','59e653e8af','cdb272d009','b03dd27d88','2c256f3025','a3652003d0','90dabc36d3'}
json.dump(sorted(S),open('/tmp/S1.json','w'))
print(len(S),subprocess.check_output(['probe','evaluate']+sorted(S)).decode())
"
```

```bash
cd /tmp; for s in "8c5053deab" "333671762b 8c5053deab" "333671762b 8c5053deab 950f45a624" "8c5053deab 950f45a624 f9cd3c6b75" "333671762b 44ef9bbd6b"; do echo "$s: $(probe evaluate $s)"; done
```

```bash
cd /tmp; python3 bfs.py 8 >/dev/null; python3 -c "
import json,subprocess;g=json.load(open('/tmp/g.json'));d=g['dist'];adj=g['adj']
def ev(s): return json.loads(subprocess.check_output(['probe','evaluate']+sorted(s)))['score']
c={}
for r in [4,5,6]:
  for name,f in [('deg>=4',lambda k:len(adj[k])>=4),('deg<=4',lambda k:len(adj[k])<=4)]:
    s=[k for k,v in d.items() if v<=r and k in adj and f(k)]
    print(r,name,len(s),ev(s))
s=[k for k,v in d.items() if v<=8];print(8,len(s),ev(s) if len(s)<=200 else '')
"
```

```bash
cd /tmp; for s in 950f45a624 f9cd3c6b75 44ef9bbd6b 74a860a8a6 59e653e8af "8c5053deab 44ef9bbd6b"; do echo "$s: $(probe evaluate $s)"; done
```

```bash
cd /tmp; python3 -c "
import json;g=json.load(open('/tmp/g.json'));d=g['dist'];adj=g['adj']
rem={'7f1652550c':0.9207,'8e67360323':0.9178,'60e0452d6b':0.9166,'41e5de6445':0.922,'77e43c04b6':0.9096,'c08448f987':0.9198,'815ba70575':0.9162,'f489ee9e06':0.9235,'1dce4a290d':0.9063,'a14c3efdea':0.9065,'0c6ef3312e':0.9079,'d361118b62':0.9144,'0255797ca1':0.9215,'7db0ec9ab4':0.9198,'32049e6a41':0.9206,'ed74ad5368':0.9228}
add={'715cfb33ce':0.9182,'7ee3b2f8c0':0.9097,'e551f27759':0.9107,'521e5d33f6':0.9202,'69ab4ee267':0.9214,'7aa610a0c0':0.9149,'71543b6fa1':0.9214,'0ac9ebe4e4':0.912,'0238aaa06c':0.9171
```

```bash
cd /tmp; cat > cand.py <<'EOF'
import json,subprocess,sys
g=json.load(open('/tmp/g.json'));d=g['dist'];adj=g['adj']
def ev(s): return json.loads(subprocess.check_output(['probe','evaluate']+sorted(s)))['score']
par={k:sum(1 for x in adj.get(k,[]) if d.get(x,99)==v-1) if k in adj else None for k,v in d.items()}
# for nodes not expanded, count parents via adjacency of expanded nodes
from collections import defaultdict
pc=defaultdict(int)
for u,nb in adj.items():
    for v in nb:
        if d.get(v)==d[u]+1: pc[v]+=1
EOF
python3 -c "
exec(open('/tmp/cand.py').read())
from collections import Count
```

```bash
cd /tmp; for s in "8c5053deab 333671762b" "333671762b 6b118e9f84" "333671762b 59e653e8af"; do echo "$s: $(probe evaluate $s)"; done
```

```bash
cd /tmp; python3 -c "
exec(open('/tmp/cand.py').read())
b5=[k for k,v in d.items() if v<=5]
for x in ['8c5053deab','333671762b','44ef9bbd6b']:
  print(x,ev([k for k in b5 if k!=x]))
"
```

```bash
cd /tmp; python3 -c "
exec(open('/tmp/cand.py').read())
far=[k for k,v in d.items() if v>=7]
print(len(far))
print('start+63far',ev(['333671762b']+far[:63]))
print('64far',ev(far[:64]))
print('far all',ev(far))
"
```

```bash
cd /tmp; python3 -c "
exec(open('/tmp/cand.py').read())
for dg in [1,2,3,5,6]:
  ks=[k for k in adj if len(adj[k])==dg and k!='333671762b'][:1]
  print(dg,ks,d[ks[0]],ev(ks))
"
```

```bash
cd /tmp; python3 -c "
exec(open('/tmp/cand.py').read())
for name,s in [('even<=6',[k for k,v in d.items() if v<=6 and v%2==0]),('odd<=6+start',['333671762b']+[k for k,v in d.items() if v<=6 and v%2==1]),('deg3',[k for k in adj if len(adj[k])==3]),('ball5 minus ball2',[k for k,v in d.items() if 3<=v<=5])]:
  print(name,len(s),ev(s))
"
```

```bash
cd /tmp; S=333671762b; for s in "$S 44ef9bbd6b 6d494d36a1" "$S 8c5053deab 44ef9bbd6b" "$S 6d494d36a1 fedb24eaeb 7f1652550c" "6d494d36a1 fedb24eaeb 7f1652550c 59e653e8af" ; do echo "$s: $(probe evaluate $s)"; done
```

```bash
cd /tmp; python3 -c "
exec(open('/tmp/cand.py').read())
for r in range(1,9):
  s=['333671762b']+[k for k,v in d.items() if v==r]
  print(r,len(s),ev(s))
"
```

```bash
cd /tmp; S=333671762b; for s in "$S 950f45a624 44ef9bbd6b" "$S f9cd3c6b75 90c7d4a4ea" "$S 8c5053deab 6b118e9f84"; do echo "$s: $(probe evaluate $s)"; done
```

```bash
probe evaluate 333671762b; probe evaluate 333671762b 8c5053deab 950f45a624 f9cd3c6b75; probe status
```

```bash
cd /tmp; python3 -c "
exec(open('/tmp/cand.py').read())
b2=[k for k,v in d.items() if v<=2]
print(ev([k for k in b2 if k!='333671762b']))
far=[k for k,v in d.items() if v>=7]
print(ev(far[:10]), ev(far[:20]))
"
```

```bash
cd /tmp; python3 -c "
exec(open('/tmp/cand.py').read())
S0='333671762b'
deg={k:len(v) for k,v in adj.items()}
res=[]
for r in [5,6,7]:
  for name,f in [('>=4',lambda x:x>=4),('==4',lambda x:x==4),('>=3',lambda x:x>=3),('<=4',lambda x:x<=4)]:
    s=set(k for k,v in d.items() if v<=r and k in deg and f(deg[k]))|{S0}
    res.append((r,name,len(s),ev(s)))
for x in res: print(x)
"
```

```bash
cd /tmp; python3 -c "
exec(open('/tmp/cand.py').read())
def ball(c,r):
  D={c:0};f=[c]
  for i in range(r):
    nf=[]
    for u in f:
      for v in adj.get(u,[]):
        if v not in D: D[v]=i+1;nf.append(v)
    f=nf
  return D
for c in ['6b118e9f84','7f1652550c']:
  B=ball(c,2); print(c,len(B),ev(B), ev([k for k in B if k!=c]))
"
```

```bash
cd /tmp; cat > wl.py <<'EOF'
import json,math
from collections import Counter
g=json.load(open('/tmp/g.json'));adj=g['adj'];dist=g['dist']
S0='333671762b'
def adjall(x):
    return adj.get(x,[])
def feats(S,h):
    S=set(S)
    lab={x:('S' if x==S0 else 'o') for x in S}
    F=Counter(lab.values())
    for i in range(h):
        nl={}
        for x in S:
            nl[x]=(lab[x],tuple(sorted(lab[y] for y in adjall(x) if y in S)))
        lab=nl;F.update(lab.values())
    return F
def cos(A,B):
    dot=sum(v*B.get(k,0) for k,v in A.items())
    return dot/math.sqrt(sum(v*v for v in A.values())*
```

```bash
cd /tmp; cat >> wl.py <<'EOF'
from collections import defaultdict
SA=defaultdict(set)
for u,nb in adj.items():
    for v in nb: SA[u].add(v);SA[v].add(u)
def adjall(x): return SA[x]
EOF
python3 -c "
exec(open('/tmp/wl.py').read())
obs=json.load(open('/tmp/obs.json'))
s=S0
b4=[k for k,v in dist.items() if v<=4]
rem={'7f1652550c':0.9207,'8e67360323':0.9178,'60e0452d6b':0.9166,'41e5de6445':0.922,'77e43c04b6':0.9096,'c08448f987':0.9198,'815ba70575':0.9162,'f489ee9e06':0.9235,'1dce4a290d':0.9063,'a14c3efdea':0.9065,'0c6ef3312e':0.9079,'d361118b62':0.9144,'0255797ca1':0.9215,'7db0ec9ab4':0.9198,'320
```

```bash
cd /tmp; cat > fit.py <<'EOF'
import random,sys
exec(open('/tmp/wl.py').read())
obs=json.load(open('/tmp/obs.json'))
h=int(sys.argv[1]); random.seed(int(sys.argv[2]))
pool=[k for k,v in dist.items() if v<=5]
FS=[(feats(S,h),sc) for S,sc in obs]
def err(T):
    FT=feats(T,h)
    return sum((cos(F,FT)-sc)**2 for F,sc in FS)
T=set(k for k,v in dist.items() if v<=3)
e=err(T);best=(e,set(T))
temp=0.01
for it in range(6000):
    x=random.choice(pool)
    if x==S0: continue
    T2=T^{x}
    e2=err(T2)
    if e2<e or random.random()<math.exp((e-e2)/temp):
        T,e=T2,e2
        if e<best[0]: best=(
```

```bash
cd /tmp; cat > fit2.py <<'EOF'
import random,sys
exec(open('/tmp/wl.py').read())
obs=json.load(open('/tmp/obs.json'))
h=int(sys.argv[1]); random.seed(int(sys.argv[2])); N=int(sys.argv[3])
pool=[k for k,v in dist.items() if v<=6 and k!=S0]
FS=[(feats(S,h),sc) for S,sc in obs]
def err(T):
    FT=feats(T,h)
    return sum((cos(F,FT)-sc)**2 for F,sc in FS)
T=set([S0]+[k for k,v in sorted(dist.items(),key=lambda x:x[1]) if k!=S0][:N-1])
e=err(T);best=(e,set(T))
temp=0.01
for it in range(8000):
    x=random.choice(sorted(T-{S0}));
    # prefer neighbors of T
    cand=[y for z in T for y in SA[z] if 
```

**agent:** h=3 with a 23-item target fits the data well (sum of squared errors ≈ 0.0012). Checking nearby sizes and comparing the fitted sets.

```bash
cd /tmp; for N in 21 22 24 25; do python3 fit2.py 3 1 $N & done; python3 fit2.py 3 3 23 & python3 fit2.py 3 4 23 & wait; python3 -c "
import json,glob
exec(open('/tmp/wl.py').read())
for f in sorted(glob.glob('/tmp/T2_3_23_*.json')):
  T=json.load(open(f)); from collections import Counter
  print(f, sorted(Counter(dist[x] for x in T).items()))
"
```

```bash
cd /tmp; python3 -c "
exec(open('/tmp/wl.py').read())
obs=json.load(open('/tmp/obs.json'))
T=json.load(open('/tmp/T2_3_24_1.json'))
from collections import Counter
print(sorted(Counter(dist[x] for x in T).items()))
FT=feats(T,3)
B3=[k for k,v in dist.items() if v<=3]
print('ball3 pred', cos(feats(B3,3),FT))
# induced structure of T
for x in sorted(T,key=lambda x:dist[x]): print(x,dist[x],len(SA[x]),[y[:4] for y in SA[x] if y in T])
"
```

```bash
cd /tmp; cat > rules.py <<'EOF'
exec(open('/tmp/wl.py').read())
obs=json.load(open('/tmp/obs.json'))
obs=[o for o in obs if max(dist[x] for x in o[0])<=7]
FS=[(feats(S,3),sc) for S,sc in obs]
def err(T):
    FT=feats(T,3); return sum((cos(F,FT)-sc)**2 for F,sc in FS)
def ball(c,r):
    D={c:0};f=[c]
    for i in range(r):
        nf=[]
        for u in f:
            for v in SA[u]:
                if v not in D: D[v]=i+1;nf.append(v)
        f=nf
    return D
res=[]
for c in adj:
    if dist[c]>5: continue
    for r in range(1,7):
        B=ball(c,r)
        if S0 in B and 10<=len(B)<=60 and 
```

```bash
cd /tmp; for f in T2_3_24_1 T2_3_25_1 T2_3_23_1; do python3 -c "
import json,subprocess;T=json.load(open('/tmp/$f.json'));print('$f',len(T),subprocess.check_output(['probe','evaluate']+T).decode().strip())"; done
```

```bash
cd /tmp; python3 -c "
exec(open('/tmp/wl.py').read())
obs=json.load(open('/tmp/obs.json'))
obs=[o for o in obs if max(dist[x] for x in o[0])<=7]
s=S0
deg={k:len(v) for k,v in adj.items()}
for f,sc in [('T2_3_24_1',.9371),('T2_3_25_1',.9224),('T2_3_23_1',.9301)]: obs.append((json.load(open(f'/tmp/{f}.json')),sc))
for r,sc in zip(range(1,9),[.4033,.4987,.5072,.5313,.6302,.6038,.6130,.6173]):
  if r<=7: obs.append(([s]+[k for k,v in dist.items() if v==r],sc))
obs.append(([k for k,v in dist.items() if v<=6 and v%2==0],.583))
obs.append(([s]+[k for k,v in dist.items() if v<=6 and v%2==1],.6256))
ob
```

**agent:** The pair-to-singleton score ratio pins the count of non-start items at 22.0 ± 0.1, so the target has exactly 23 items. Running longer fits at N=23.

```bash
cd /tmp; sed -i 's/range(8000)/range(int(sys.argv[4]))/; s/temp\*=0.999/temp*=0.9995/' fit2.py; for s in 11 12 13 14 15 16 17 18; do python3 fit2.py 3 $s 23 15000 & done; wait
```

```bash
cd /tmp; python3 -c "
exec(open('/tmp/wl.py').read())
T=json.load(open('/tmp/T3_3_23_12.json'))
from collections import Counter
print(sorted(Counter(dist[x] for x in T).items()))
F=feats(T,3)
for x in sorted(T,key=lambda x:dist[x]): print(x[:4],dist[x],[y[:4] for y in SA[x] if y in T])
e=sum(1 for x in T for y in SA[x] if y in T)//2; print('edges',e)
"; python3 -c "
import json,subprocess;T=json.load(open('/tmp/T3_3_23_12.json'));print(subprocess.check_output(['probe','evaluate']+T).decode())"
```

**agent:** Best fit scores 0.954 for real. Before spending more evaluations, I'll check structured rule families with the model: degree-restricted balls and components around the start.

```bash
cd /tmp; cat > rules2.py <<'EOF'
exec(open('/tmp/wl.py').read())
obs=json.load(open('/tmp/obs2.json'))
obs.append((json.load(open('/tmp/T3_3_23_12.json')),.9538))
json.dump(obs,open('/tmp/obs3.json','w'))
FS=[(feats(S,3),sc) for S,sc in obs]
def err(T):
    FT=feats(T,3); return sum((cos(F,FT)-sc)**2 for F,sc in FS)
deg={k:len(SA[k]) for k in adj}
def ballf(r,ok):
    D={S0:0};f=[S0]
    for i in range(r):
        nf=[]
        for u in f:
            for v in SA[u]:
                if v not in D and v in deg and ok(v): D[v]=i+1;nf.append(v)
        f=nf
    return D
import itertools
res=[]
de
```

**agent:** Simple degree/distance rules fit badly (error ≈ 0.047 vs ≈ 0.0003 for the fitted sets), so I'll stick with the structural fit and iterate.

```bash
cd /tmp; cat > fit3.py <<'EOF'
import random,sys
exec(open('/tmp/wl.py').read())
obs=json.load(open('/tmp/obs3.json'))
h=3; random.seed(int(sys.argv[1])); N=23
pool=[k for k,v in dist.items() if v<=7 and k!=S0]
FS=[(feats(S,h),sc) for S,sc in obs]
def err(T):
    FT=feats(T,h)
    return sum((cos(F,FT)-sc)**2 for F,sc in FS)
init=sys.argv[2]
T=set(json.load(open(init))) if init!='-' else set([S0]+[k for k,v in sorted(dist.items(),key=lambda x:x[1]) if k!=S0][:N-1])
e=err(T);best=(e,set(T))
temp=float(sys.argv[3])
for it in range(int(sys.argv[4])):
    x=random.choice(sorted(T-{S0}))
    cand=[
```

**agent:** Each score is a linear measurement of the target's WL feature counts (dot = score·|F_S|·Z, with Z ≈ 26.265 from the singleton/pair data). Iterating fits, starting from the current best solutions.

```bash
cd /tmp; nproc; for s in 21 22 23 24; do python3 fit3.py $s /tmp/T3_3_23_12.json 0.0005 40000 & done; for s in 25 26 27 28; do python3 fit3.py $s /tmp/R_4.json 0.0005 40000 & done; wait
```

```bash
cd /tmp; python3 -c "import scipy,numpy;print(scipy.__version__)"; python3 -c "
exec(open('/tmp/wl.py').read())
obs=json.load(open('/tmp/obs3.json'))
Z=26.265
from collections import Counter
# level-1 only features
def f1(S):
  S=set(S);c=Counter()
  for x in S:
    l='S' if x==S0 else 'o'
    nb=sorted('S' if y==S0 else 'o' for y in SA[x] if y in S)
    c[(l,tuple(nb))]+=1
  return c
allf=set()
for S,sc in obs: allf|=set(f1(S))
print(len(allf),sorted(allf))
"
```

```bash
cd /tmp; sed -e "s#T=set(json.load(open(init))) if init!='-' else .*#T={S0}\n    \nwhile len(T)<N:\n    T.add(random.choice([y for z in T for y in SA[z] if y not in T and y in dist and dist[y]<=7]))#" -e "s#open(f'/tmp/R_#open(f'/tmp/Q_#" fit3.py > fit4.py; sed -n '10,16p' fit4.py; for s in $(seq 100 163); do python3 fit4.py $s - 0.003 30000 > /tmp/q_$s.log & done; wait; sort -g /tmp/q_*.log | head -5
```

