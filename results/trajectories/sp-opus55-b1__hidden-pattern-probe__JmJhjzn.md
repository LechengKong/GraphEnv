# sp-opus55-b1 / hidden-pattern-probe__JmJhjzn

model=bedrock/us.anthropic.claude-opus-5-5 reward=0.0 exception=None evaluate=146 best=0.9659

```bash
probe --help; probe status
```

**agent:** Let me BFS the graph since neighbors is free.

```bash
probe neighbors b8926eb97b; mkdir -p /tmp/w && cat > /tmp/w/bfs.py <<'EOF'
import json,subprocess
s="b8926eb97b"
adj={};dist={s:0};q=[s]
while q:
    u=q.pop(0)
    out=json.loads(subprocess.check_output(["probe","neighbors",u]))
    nb=out if isinstance(out,list) else out.get("neighbors",out)
    adj[u]=nb
    for v in nb:
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
json.dump({"adj":adj,"dist":dist},open("/tmp/w/g.json","w"))
from collections import Counter
print(len(dist),Counter(dist.values()))
EOF
python3 /tmp/w/bfs.py
```

```bash
cd /tmp/w; for r in 0 1 2 3; do python3 -c "
import json;d=json.load(open('g.json'))['dist']
print('\n'.join(k for k,v in d.items() if v<=$r))" | probe evaluate -; echo; done
```

```bash
cd /tmp/w; for r in 4 5 6; do python3 -c "
import json;d=json.load(open('g.json'))['dist']
print('\n'.join(k for k,v in d.items() if v<=$r))" | probe evaluate -; echo; done
```

```bash
cd /tmp/w; python3 -c "
import json;g=json.load(open('g.json'));a=g['adj'];d=g['dist']
from collections import Counter
print(Counter(len(v) for v in a.values()))
for r in range(7):
  print(r,sorted(len(a[k]) for k,v in d.items() if v==r))
"
```

```bash
cd /tmp/w; s=b8926eb97b; for n in 40234ca2ac 7177bc61e3 91b3c0bda3 e6f6a117af; do probe evaluate $s $n; echo; done; probe evaluate 40234ca2ac
```

```bash
cd /tmp/w; python3 -c "
import json;g=json.load(open('g.json'));d=g['dist']
for r in [2,3,5,8]: print([k for k,v in d.items() if v==r][0])
" | while read x; do probe evaluate $x; echo; done
```

```bash
cd /tmp/w; python3 -c "
import json;g=json.load(open('g.json'));d=g['dist']
f=[k for k,v in d.items() if v>=40]
print(f[0],f[1],f[2])
"
```

```bash
probe evaluate 68e03f2324 998b0a6dbb; echo; probe evaluate b8926eb97b 68e03f2324; echo; probe evaluate 68e03f2324 998b0a6dbb e595406c14
```

```bash
s=b8926eb97b; probe evaluate $s 68e03f2324 998b0a6dbb; echo; probe evaluate $s 40234ca2ac 7177bc61e3; echo; probe evaluate $s 40234ca2ac 68e03f2324
```

```bash
s=b8926eb97b; probe evaluate $s 40234ca2ac 68e03f2324; echo; probe evaluate $s 68e03f2324 40234ca2ac
```

```bash
cd /tmp/w; python3 -c "
import json,random;g=json.load(open('g.json'));d=g['dist']
random.seed(1);f=[k for k,v in d.items() if v>=20]
print('\n'.join(['b8926eb97b']+random.sample(f,12)))" | probe evaluate -; echo
python3 -c "
import json,random;g=json.load(open('g.json'));d=g['dist']
random.seed(1);f=[k for k,v in d.items() if v>=20]
print('\n'.join(['b8926eb97b']+random.sample(f,60)))" | probe evaluate -
```

```bash
cd /tmp/w; python3 -c "
import json;g=json.load(open('g.json'));a=g['adj']
asym=sum(1 for u in a for v in a[u] if u not in a[v]);print('asym',asym)
print(sum(len(v) for v in a.values())//2)
"
```

```bash
cd /tmp/w; cat > ev.py <<'EOF'
import json,subprocess,sys
g=json.load(open('/tmp/w/g.json'));d=g['dist'];a=g['adj']
def ev(S):
    out=subprocess.run(["probe","evaluate","-"],input="\n".join(S),capture_output=True,text=True).stdout
    return json.loads(out)["score"]
EOF
python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ev import *
B=[k for k,v in d.items() if v<=5]
L5=[k for k,v in d.items() if v==5]
for x in L5[:4]:
  print(x,len(a[x]),ev([y for y in B if y!=x]))
"
```

```bash
cd /tmp/w; python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ev import *
B=[k for k,v in d.items() if v<=5]
for x in [k for k,v in d.items() if v==5][4:]:
  print('rm5',x,len(a[x]),ev([y for y in B if y!=x]))
for x in [k for k,v in d.items() if v==6]:
  print('add6',x,len(a[x]),ev(B+[x]))
" | tee l56.txt
```

```bash
cd /tmp/w; python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ev import *
base=0.9339
L=[l.split() for l in open('l56.txt')]
B=[k for k,v in d.items() if v<=5]
rm=['3879ab56f9','6bebb8b1c5','2b5cf5e0b5']+[x for t,x,_,s in L if t=='rm5' and float(s)>base]
ad=[x for t,x,_,s in L if t=='add6' and float(s)>base]
S=[y for y in B if y not in rm]
print(len(S),ev(S)); print(len(S+ad),ev(S+ad))
"
```

```bash
cd /tmp/w; python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ev import *
B=[k for k,v in d.items() if v<=5]
for x in ['40234ca2ac']+[k for k,v in d.items() if v==3][:2]:
  print(x,ev([y for y in B if y!=x]))
"
```

```bash
cd /tmp/w; python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ev import *
B=[k for k,v in d.items() if v<=5]
print(ev([y for y in B if y!='b8926eb97b']))
print(ev([k for k,v in d.items() if v<=1 and k!='b8926eb97b']))
"
```

```bash
cd /tmp/w; python3 -c "
import sys,random;sys.path.insert(0,'/tmp/w')
from ev import *
random.seed(1);f=[k for k,v in d.items() if v>=20]
print(ev(random.sample(f,60)))
L=[k for k,v in d.items() if v==2]
print(ev(L))
print(ev(['b8926eb97b']+L))
"
```

```bash
cd /tmp/w; python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ev import *
out='3879ab56f9 6bebb8b1c5 2b5cf5e0b5 ea75e8eaed 08ba56830b bd41658532 5d872afa55 491b1446f4 7a7b0c5b39'.split()
inn='f073e9ede0 3a53083139 1e6c93952f 21be3846ae 482361a719 79774be962 eca8b01ecf c5bf44513a 8f6dd851fd 4b309a8942 9a83788fa9 40234ca2ac'.split()
def f(x):
  n=a[x];tri=sum(1 for i in n for j in n if i<j and j in a[i])
  par=sum(1 for y in n if d[y]<d[x]);same=sum(1 for y in n if d[y]==d[x])
  return (d[x],len(n),tri,par,same,sorted(len(a[y]) for y in n))
for x in out: print('OUT',x,f(x))
for x in inn: p
```

```bash
cd /tmp/w; python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ev import *
B=[k for k,v in d.items() if v<=5]
print(ev(B+['68e03f2324']))
print(ev(B+['68e03f2324','998b0a6dbb']))
"
```

```bash
cd /tmp/w; cat > greedy.py <<'EOF'
import sys,json;sys.path.insert(0,'/tmp/w')
from ev import *
st=json.load(open('/tmp/w/state.json'))
S=set(st['S']);best=st['best']
for x in sys.argv[1:]:
    T=S^{x}
    sc=ev(sorted(T))
    print(x,d[x],'in' if x in S else 'out',sc,flush=True)
    if sc>best: S,best=T,sc
    json.dump({'S':sorted(S),'best':best},open('/tmp/w/state.json','w'))
print('best',best,len(S))
EOF
python3 -c "
import sys,json;sys.path.insert(0,'/tmp/w')
from ev import *
S=[y for y in d if d[y]<=5 and y!='491b1446f4']
json.dump({'S':S,'best':0.9409},open('/tmp/w/state.json','w'))
pri
```

```bash
cd /tmp/w; python3 -c "
import sys,json;sys.path.insert(0,'/tmp/w')
from ev import *
S=json.load(open('state.json'))['S']
from collections import Counter
print(Counter(d[x] for x in S))
print([x for x in d if d[x]<=5 and x not in S])
"
```

```bash
cd /tmp/w; python3 -c "
import sys,json;sys.path.insert(0,'/tmp/w')
from ev import *
S=set(json.load(open('state.json'))['S'])
for n in a['b8926eb97b']:
  print(n,len(a[n]),[(c,d[c],c in S,len(a[c])) for c in a[n] if d[c]==2])
"
```

```bash
probe status
```

```bash
cd /tmp/w; python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ev import *
for mx in [4,5]:
 for r in [5,6]:
  S=[x for x in d if d[x]<=r and (len(a[x])<=mx or x=='b8926eb97b')]
  print(mx,r,len(S),ev(S))
"
```

```bash
cd /tmp/w; python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ev import *
s='b8926eb97b'
def rb(r,mx):
  D={s:0};q=[s]
  while q:
    u=q.pop(0)
    if D[u]==r: continue
    for v in a[u]:
      if v not in D and len(a[v])<=mx: D[v]=D[u]+1;q.append(v)
  return D
for r in [5,6]:
  D=rb(r,5);S=list(D);S2=[x for x in d if d[x]<=r and len(a[x])<=5]
  print(r,len(S),len(S2),set(S2)^set(S))
"
```

```bash
cd /tmp/w; python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ev import *
s='b8926eb97b'
def rb(r,mx):
  D={s:0};q=[s]
  while q:
    u=q.pop(0)
    if D[u]==r: continue
    for v in a[u]:
      if v not in D and len(a[v])<=mx: D[v]=D[u]+1;q.append(v)
  return D
for r in [5,6,7]:
  S=list(rb(r,5));print(r,len(S),ev(S))
"
```

```bash
cd /tmp/w; cat > ppr.py <<'EOF'
import sys;sys.path.insert(0,'/tmp/w')
from ev import *
s='b8926eb97b'
def ppr(al,it=200):
    p={s:1.0};r={x:0 for x in d}
    v={x:0.0 for x in d};v[s]=1
    x=dict(v)
    for _ in range(it):
        nx={k:0.0 for k in d}
        for u,val in x.items():
            if val==0: continue
            for w in a[u]: nx[w]+=(1-al)*val/len(a[u])
        nx[s]+=al
        x=nx
    return x
EOF
python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ppr import *
x=ppr(0.15);R=sorted(d,key=lambda k:-x[k])
B5=set(k for k in d if d[k]<=5 and len(a[k])<=5)
for K in [54,60
```

```bash
cd /tmp/w; python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ppr import *
for al in [0.15]:
  x=ppr(al);R=sorted(d,key=lambda k:-x[k])
  for K in [50,60,70]: print(al,K,ev(R[:K]))
"
```

```bash
cd /tmp/w; python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ppr import *
x=ppr(0.15);R=sorted(d,key=lambda k:-x[k]/len(a[k]))
from collections import Counter
for K in [55]: print(K,Counter(d[k] for k in R[:K]),ev(R[:K]))
"
```

```bash
cd /tmp/w; python3 -c "
import json
g=json.load(open('g.json'));d=g['dist'];a=g['adj']
S=[x for x in d if d[x]<=5 and len(a[x])<=5]
json.dump({'S':S,'best':0.959},open('state.json','w'))"
python3 greedy.py 491b1446f4 02ac8fd827 f5627a7cb1 4a7b0c9fbd 1637e1ed3d d896841ad9
```

```bash
cd /tmp/w; python3 -c "
import sys;sys.path.insert(0,'/tmp/w')
from ev import *
s='b8926eb97b'
D={s:0};q=[s]
while q:
  u=q.pop(0)
  if D[u]==6 : continue
  for v in a[u]:
    if v not in D and len(a[v])<=5: D[v]=D[u]+1;q.append(v)
S=[x for x in D if True]
S2=[x for x in d if d[x]<=6 and len(a[x])<=5 and d[x]<=5 or x in ('1637e1ed3d','d896841ad9')]
print(len(S2))
import json;st=json.load(open('state.json'));print(set(st['S'])^set(S2))
"
```

```bash
cd /tmp/w; python3 greedy.py d896841ad9 14bde48054 ea75e8eaed 3879ab56f9 6bebb8b1c5 5d872afa55 5c5793c7f9 7a7b0c5b39
```

```bash
cd /tmp/w; python3 -c "
import sys,json;sys.path.insert(0,'/tmp/w')
from ev import *
st=json.load(open('state.json'));S=set(st['S'])
T=[x for x in S if len(a[x])>=3 or x=='b8926eb97b'];print(len(S)-len(T),ev(T))
"
```

```bash
cd /tmp/w; python3 -c "
import json;print('\n'.join(json.load(open('state.json'))['S']))" | probe submit -
```

**agent:** I submitted a 54-item selection, but it almost certainly does not match the target. Its best `evaluate` score was **0.9659**, I never got a 1.0, and the task grades anything short of an exact match as zero.

**What I learned**
- **Graph shape:** following links from the start item reaches 1,599 items. Links run both ways, and most items have 2–6 neighbours.
- **Scores by distance:** I scored every item within N steps of the start, for N from 0 to 6. The scores were 0.015, 0.41, 0.83, 0.90, 0.90, 0.93 and 0.91. The best was everything within 5 steps, at 0.934, so the target is roughly that area but not exactly it.
- **Puzzling scores:** the scoring doesn't act like plain overlap with the target.
  - Any small selection without the start item scored exactly 0.4154, wherever its items were.
  - The start item alone scored only 0.0148.
  - Removing items next to the start sometimes raised the score, and changing one item usually moved it by less than 0.01.
- **Best rule I found:** everything within 5 steps that has at most 5 neighbours scored 0.959. Adding or removing single items from there got me to 0.9659.
- **Rules that scored lower:**
  - a search that doesn't pass through items with 6 or more neighbours (0.93–0.95)
  - a stricter limit of 4 neighbours (0.91)
  - a ranking based on random walks from the start (about 0.92–0.93)

**What went wrong**
I spent about 60 of the 150 evaluations testing one item at a time. The scores interact with each other, so those results didn't add up to a useful picture. That left too little budget to pin down the rule.

The final selection is the within-5-steps, at-most-5-neighbours set, minus one item (`491b1446f4`) and plus one item (`1637e1ed3d`). Unless that happens to be exactly the target, it will score zero.

