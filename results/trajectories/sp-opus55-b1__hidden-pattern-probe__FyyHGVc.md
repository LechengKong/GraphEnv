# sp-opus55-b1 / hidden-pattern-probe__FyyHGVc

model=bedrock/us.anthropic.claude-opus-5-5 reward=1.0 exception=None evaluate=109 best=1.0

```bash
probe --help; probe status
```

**agent:** Let me crawl the graph via BFS (neighbors is free).

```bash
mkdir -p /tmp/w && cd /tmp/w && probe neighbors b8926eb97b; cat > crawl.py <<'EOF'
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
    if len(adj)>5000: break
json.dump({"adj":adj,"dist":dist},open("g.json","w"))
print(len(adj),len(dist),collections.Counter(dist.values()))
EOF
python3 crawl.py
```

```bash
cd /tmp/w && python3 -c "
import json;g=json.load(open('g.json'));a=g['adj']
asym=sum(1 for u in a for v in a[u] if u not in a.get(v,[]))
print('asym',asym)
import collections;print(collections.Counter(len(v) for v in a.values()))
"
for r in 1 2 3; do python3 -c "
import json;g=json.load(open('g.json'))
print('\n'.join(k for k,d in g['dist'].items() if d<=$r))" | probe evaluate -; done
```

```bash
cd /tmp/w && for r in 4 5; do python3 -c "
import json;g=json.load(open('g.json'))
print('\n'.join(k for k,d in g['dist'].items() if d<=$r))" | probe evaluate -; done
```

```bash
cd /tmp/w && probe evaluate b8926eb97b; for r in 6 8; do python3 -c "
import json;g=json.load(open('g.json'))
print('\n'.join(k for k,d in g['dist'].items() if d<=$r))" | probe evaluate -; done
```

```bash
cd /tmp/w && python3 -c "
import json;g=json.load(open('g.json'))
for r in range(10): print(r,sum(1 for d in g['dist'].values() if d<=r))"
```

```bash
cd /tmp/w && python3 -c "
import json;g=json.load(open('g.json'));d=g['dist']
far=[k for k,v in d.items() if v==20][:2];print(far)
print(g['adj']['b8926eb97b'])
" 
```

```bash
cd /tmp/w && probe evaluate 40234ca2ac; probe evaluate 162d0abeba; probe evaluate b8926eb97b 162d0abeba; probe evaluate b8926eb97b 40234ca2ac
```

```bash
cd /tmp/w && probe evaluate 40234ca2ac 7177bc61e3; probe evaluate 162d0abeba 610a9500ea; probe evaluate 40234ca2ac 7177bc61e3 91b3c0bda3 e6f6a117af; probe evaluate 7177bc61e3
```

```bash
cd /tmp/w && probe evaluate b8926eb97b 162d0abeba 610a9500ea; probe evaluate b8926eb97b 40234ca2ac 7177bc61e3
```

```bash
cd /tmp/w && for i in 1 2; do probe evaluate b8926eb97b 40234ca2ac 7177bc61e3; done; probe evaluate b8926eb97b 7177bc61e3 40234ca2ac
```

```bash
cd /tmp/w && cat > ev.py <<'EOF'
import json,subprocess,sys,random
g=json.load(open('/tmp/w/g.json'));d=g['dist']
def ev(items):
    items=list(dict.fromkeys(items))
    o=subprocess.run(["probe","evaluate","-"],input="\n".join(items),capture_output=True,text=True).stdout
    return json.loads(o)["score"]
EOF
cat > t1.py <<'EOF'
exec(open('/tmp/w/ev.py').read())
s="b8926eb97b";random.seed(1)
far=[k for k,v in d.items() if v>=25]
for k in [2,4]:
    sh=[x for x,v in d.items() if v==k]
    print(k,len(sh),ev([s]+sh),ev([s]+random.sample(far,len(sh))))
EOF
python3 t1.py
```

```bash
cd /tmp/w && cat > t2.py <<'EOF'
exec(open('/tmp/w/ev.py').read())
B=[x for x,v in d.items() if v<=8]
for k in range(1,9):
    print(k,ev([x for x in B if d[x]!=k]))
EOF
python3 t2.py
```

```bash
cd /tmp/w && cat > t3.py <<'EOF'
exec(open('/tmp/w/ev.py').read())
s="b8926eb97b"
for lo,hi in [(5,8),(5,9),(5,10),(6,9),(7,10),(3,10)]:
    print(lo,hi,ev([s]+[x for x,v in d.items() if lo<=v<=hi]))
EOF
python3 t3.py
```

```bash
cd /tmp/w && cat > t4.py <<'EOF'
exec(open('/tmp/w/ev.py').read())
s="b8926eb97b";random.seed(2)
B=[x for x,v in d.items() if v<=2]
far=[k for k,v in d.items() if v>=25]
print('b2+8far',ev(B+random.sample(far,8)))
for x in B[1:]:
    print(x,d[x],ev([y for y in B if y!=x]))
EOF
python3 t4.py
```

```bash
cd /tmp/w && cat > t5.py <<'EOF'
exec(open('/tmp/w/ev.py').read())
s="b8926eb97b";a=g['adj']
import collections
bydeg=collections.defaultdict(list)
for x,v in d.items():
    if v>=10: bydeg[len(a[x])].append(x)
for k in sorted(bydeg): print(k, ev([s,bydeg[k][0]]))
print('start deg',len(a[s]),[len(a[x]) for x in a[s]])
EOF
python3 t5.py
```

```bash
cd /tmp/w && cat > t6.py <<'EOF'
exec(open('/tmp/w/ev.py').read())
s="b8926eb97b";a=g['adj']
def comp(pred):
    seen={s};st=[s]
    while st:
        u=st.pop()
        for v in a[u]:
            if v not in seen and pred(v): seen.add(v);st.append(v)
    return seen
D=lambda x:len(a[x])
for name,p in [('eq4',lambda x:D(x)==4),('ge4',lambda x:D(x)>=4),('le4',lambda x:D(x)<=4),('ge3',lambda x:D(x)>=3),('le5',lambda x:D(x)<=5),('3to5',lambda x:3<=D(x)<=5)]:
    c=comp(p);print(name,len(c),max(d[x] for x in c))
EOF
python3 t6.py
```

```bash
cd /tmp/w && cat >> t6.py <<'EOF'
print(ev(list(comp(lambda x:D(x)==4))))
EOF
python3 t6.py
```

```bash
cd /tmp/w && python3 -c "
exec(open('/tmp/w/ev.py').read())
B=[x for x,v in d.items() if 1<=v<=5]
print(len(B),ev(B))
B=[x for x,v in d.items() if v<=5]
print(ev(B+B[:0]), ev(B[:1]+B[5:]))
"
```

```bash
cd /tmp/w && python3 -c "
exec(open('/tmp/w/ev.py').read())
random.seed(3)
s='b8926eb97b'
far=[k for k,v in d.items() if v>=12]
print(ev([s]+random.sample(far,140)))
print(ev([s]+random.sample(far,60)))
print(ev([x for x,v in d.items() if v<=9]))
"
```

```bash
cd /tmp/w && python3 -c "
exec(open('/tmp/w/ev.py').read())
s='b8926eb97b'
B2=[x for x,v in d.items() if v<=2]
print(ev(B2[1:]))
B1=[x for x,v in d.items() if v<=1]
print(ev(B1[1:]+[x for x,v in d.items() if v==2][:1]))
print(ev([x for x,v in d.items() if v==2]))
"
```

```bash
cd /tmp/w && python3 -c "
exec(open('/tmp/w/ev.py').read())
B2=[x for x,v in d.items() if v<=2]
print(ev(B2[::-1]), ev(sorted(B2)))
print(B2)
"
```

```bash
cd /tmp/w && cat > t7.py <<'EOF'
exec(open('/tmp/w/ev.py').read())
exec(open('/tmp/w/t6.py').read().split('for name')[0])
s="b8926eb97b";random.seed(4)
C=comp(lambda x:D(x)>=4)
inC=[x for x in C if x!=s]; out=[x for x in d if x not in C]
print(ev([s]+random.sample(inC,150)), ev([s]+random.sample(out,150)))
EOF
python3 t7.py
```

```bash
cd /tmp/w && cat > t8.py <<'EOF'
exec(open('/tmp/w/ev.py').read())
import collections
a=g['adj']
def ball(c,r):
    dd={c:0};q=collections.deque([c])
    while q:
        u=q.popleft()
        if dd[u]==r: continue
        for v in a[u]:
            if v not in dd: dd[v]=dd[u]+1;q.append(v)
    return list(dd)
c='162d0abeba'
for r in [2,5]:
    b=ball(c,r);print(r,len(b),ev(b))
EOF
python3 t8.py
```

```bash
cd /tmp/w && python3 -c "
exec(open('/tmp/w/ev.py').read())
a=g['adj'];c='162d0abeba'
n=a[c][0]
print(ev([c,n]))
print(ev([c]+a[c]), len(a[c]))
print(ev(['40234ca2ac']+a['40234ca2ac']), a['40234ca2ac'])
"
```

```bash
cd /tmp/w && python3 -c "
exec(open('/tmp/w/ev.py').read())
a=g['adj'];c='162d0abeba';s='b8926eb97b'
st=[c]+a[c]
print(ev(st+[s]))
print(ev(st+['40234ca2ac']))
print(ev(st[:3]), ev(st[:4]), ev(st[1:]))
"
```

```bash
cd /tmp/w && cat >> t8.py <<'EOF'
random.seed(7)
nodes=list(d)
for i in range(8):
    c=random.choice(nodes);b=ball(c,2)
    print(d[c],len(b),len(a[c]),ev(b))
EOF
sed -i 's/^for r in \[2,5\]:/for r in []:/' t8.py; python3 t8.py
```

```bash
cd /tmp/w && probe status; python3 -c "
exec(open('/tmp/w/ev.py').read())
for r in [3,4,6,8]:
    print(r,ev([x for x,v in d.items() if 1<=v<=r]))
"
```

```bash
cd /tmp/w && python3 -c "
exec(open('/tmp/w/ev.py').read())
a=g['adj']
# find another node of degree 4 far, take its 4 nbrs; check no edges among nbrs
for x in d:
    if len(a[x])==4 and d[x]>25:
        nb=a[x]
        if all(v not in a[u] for u in nb for v in nb):
            print(x,d[x],ev(nb),ev([x]+nb)); break
random.seed(9)
far=random.sample([k for k,v in d.items() if v>=15],4);print(ev(far))
"
```

```bash
cd /tmp/w && python3 -c "
exec(open('/tmp/w/ev.py').read())
a=g['adj'];c='162d0abeba'
for x in a[c]: print(x,len(a[x]),ev([x]))
"
```

```bash
cd /tmp/w && python3 -c "
import json;g=json.load(open('g.json'));a=g['adj']
L=['252693b05c','610a9500ea','8bedf3e222','91a579111a']
print([(u,v) for u in L for v in L if v in a[u]])
for x in L: print(x,a[x])
"
```

```bash
cd /tmp/w && cat > data.py <<'EOF'
import json,random,collections
g=json.load(open('/tmp/w/g.json'));d=g['dist'];a=g['adj']
s="b8926eb97b";c='162d0abeba'
def ball(c,r):
    dd={c:0};q=collections.deque([c])
    while q:
        u=q.popleft()
        if dd[u]==r: continue
        for v in a[u]:
            if v not in dd: dd[v]=dd[u]+1;q.append(v)
    return list(dd)
B=lambda r:[x for x,v in d.items() if v<=r]
D=[]
for r,sc in zip(range(1,7),[.4066,.833,.9024,.8952,.9339,.9096]): D.append((B(r),sc))
D.append((B(8),.9329)); D.append((B(9),.9393))
D+=[([s],.0148),(['40234ca2ac'],.4154),([s,c],.30
```

```bash
pip install scipy -q 2>&1 | tail -1; cd /tmp/w && python3 fit.py
```

```bash
cd /tmp/w && python3 -c "
exec(open('/tmp/w/data.py').read())
def m(S):
    S=set(S);return sum(v in S for x in S for v in a[x])//2
for S,sc in D[:40]: print(len(S),m(S),s in S,sc)
"
```

```bash
cd /tmp/w && cat > model.py <<'EOF'
exec(open('/tmp/w/data.py').read())
import numpy as np
def ideg(S):
    S=set(S);return collections.Counter(sum(v in S for v in a[x]) for x in S)
def cos(h1,h2):
    ks=set(h1)|set(h2);v1=np.array([h1.get(k,0) for k in ks],float);v2=np.array([h2.get(k,0) for k in ks],float)
    return v1@v2/np.linalg.norm(v1)/np.linalg.norm(v2)
y=np.array([sc for _,sc in D])
for r in range(1,12):
    T=B(r);hT=ideg(T)
    p=np.array([cos(ideg(S),hT) for S,_ in D])
    print(r,len(T),np.corrcoef(p,y)[0,1],np.abs(p-y).mean())
EOF
python3 model.py
```

```bash
cd /tmp/w && cat > fit2.py <<'EOF'
exec(open('/tmp/w/data.py').read())
import numpy as np
y=np.array([sc for _,sc in D])
def run(name,f,steps=20000):
    H=[collections.Counter(f(x,set(S)) for x in S) for S,_ in D]
    keys=sorted(set().union(*H),key=str);K={k:i for i,k in enumerate(keys)}
    X=np.zeros((len(D),len(keys)))
    for i,h in enumerate(H):
        for k,v in h.items(): X[i,K[k]]=v
    Xn=X/np.linalg.norm(X,axis=1,keepdims=True)
    best=1e9
    for rep in range(3):
        w=np.random.rand(len(keys));lr=0.05
        for t in range(steps):
            n=np.linalg.norm(w);p=Xn@w/n;r
```

```bash
cd /tmp/w && cat >> fit2.py <<'EOF'
print('----')
def ideg2(x,S): return sum(v in S and v!=s for v in a[x])
def tri(x,S):
    nb=[v for v in a[x] if v in S]
    return sum(1 for i in range(len(nb)) for j in range(i) if nb[j] in a[nb[i]])
run('ideg_nostart',lambda x,S:'S' if x==s else ideg2(x,S))
run('tri',lambda x,S:'S' if x==s else tri(x,S))
run('tri_raw',lambda x,S:tri(x,S))
run('ideg_tri',lambda x,S:'S' if x==s else (ideg2(x,S),tri(x,S)))
EOF
sed -i 's/^k,w=run/#k,w=run/; s/^for kk/#for kk/' fit2.py; python3 fit2.py
```

```bash
cd /tmp/w && cat > t9.py <<'EOF'
exec(open('/tmp/w/data.py').read())
exec(open('/tmp/w/ev.py').read())
import itertools
def path3(center):
    nb=a[center]
    for u,v in itertools.combinations(nb,2):
        if v not in a[u]: return [u,center,v]
def tri(center):
    nb=a[center]
    for u,v in itertools.combinations(nb,2):
        if v in a[u]: return [u,center,v]
far=[x for x,v in d.items() if v>=15]
random.seed(11);cs=random.sample(far,6)
p1=path3(cs[0]);p2=path3(cs[1])
print('path3',ev(p1))
print('2paths',ev(p1+p2))
print('tri',ev(tri(cs[2])))
print('path3+iso',ev(p1+[cs[3]]))
EOF
python3 
```

```bash
cd /tmp/w && probe status; cat > t10.py <<'EOF'
exec(open('/tmp/w/data.py').read())
exec(open('/tmp/w/ev.py').read())
import itertools
far=[x for x,v in d.items() if v>=15]
def find(pred):
    for x in far:
        r=pred(x)
        if r: return r
def tri(c):
    for u,v in itertools.combinations(a[c],2):
        if v in a[u]: return [u,c,v]
def k13(c):
    for t in itertools.combinations(a[c],3):
        if all(y not in a[x] for x,y in itertools.combinations(t,2)): return [c,*t]
def p4(c):
    for u in a[c]:
        for v in a[c]:
            if v==u or v in a[u]: continue
            for w i
```

```bash
cd /tmp/w && cat > wl.py <<'EOF'
exec(open('/tmp/w/data.py').read())
import numpy as np
def wl(S,h):
    S=set(S);lab={x:('S' if x==s else 'L') for x in S};C=collections.Counter((0,l) for l in lab.values())
    for it in range(1,h+1):
        lab={x:(lab[x],tuple(sorted(lab[v] for v in a[x] if v in S))) for x in S}
        lab={x:hash(l) for x,l in lab.items()}
        C.update((it,l) for l in lab.values())
    return C
def cos(c1,c2):
    num=sum(v*c2.get(k,0) for k,v in c1.items())
    return num/np.sqrt(sum(v*v for v in c1.values())*sum(v*v for v in c2.values()))
y=np.array([sc for _,sc in 
```

```bash
cd /tmp/w && python3 -c "
exec(open('/tmp/w/wl.py').read().split('if __name__')[0])
T=B(3)
for h in [2,3,5]:
  hT=wl(T,h)
  print(h,[ (round(cos(wl(S,h),hT),4),sc) for S,sc in D[:28]])
"
```

```bash
cd /tmp/w && cat > cand.py <<'EOF'
exec(open('/tmp/w/wl.py').read().split('if __name__')[0])
Dg=lambda x:len(a[x])
def cbfs(r,p):
    dd={s:0};q=collections.deque([s])
    while q:
        u=q.popleft()
        if dd[u]==r: continue
        for v in a[u]:
            if v not in dd and p(v): dd[v]=dd[u]+1;q.append(v)
    return list(dd)
cands={}
preds={'ge%d'%k:(lambda k:lambda x:Dg(x)>=k)(k) for k in range(2,6)}
preds.update({'le%d'%k:(lambda k:lambda x:Dg(x)<=k)(k) for k in range(2,6)})
preds.update({'eq%d'%k:(lambda k:lambda x:Dg(x)==k)(k) for k in range(2,6)})
preds.update({'ne%d'%k:(lambd
```

```bash
cd /tmp/w && cat > ls.py <<'EOF'
exec(open('/tmp/w/wl.py').read().split('if __name__')[0])
import sys
h=int(sys.argv[1]);random.seed(int(sys.argv[2]))
WS=[wl(S,h) for S,_ in D]
def err(T):
    hT=wl(T,h);p=np.array([cos(w,hT) for w in WS]);return np.sum((p-y)**2)
T=set(B(3));E=err(T)
pool=B(6)
for it in range(3000):
    T2=set(T)
    x=random.choice(pool)
    if x==s: continue
    if x in T2: T2.remove(x)
    else: T2.add(x)
    e=err(T2)
    if e<=E: T,E=T2,e
print(h,E,len(T),sorted(collections.Counter(d[x] for x in T).items()))
json.dump(sorted(T),open('/tmp/w/fit_%d_%s.json'%(h,sys.argv[2])
```

```bash
cd /tmp/w && sed -i 's/range(3000)/range(int(sys.argv[3]))/' ls.py && for sd in 2 3 4 5; do python3 ls.py 3 $sd 8000 & done; wait
```

```bash
cd /tmp/w && cat > sa.py <<'EOF'
exec(open('/tmp/w/wl.py').read().split('if __name__')[0])
import sys,math
h=3;random.seed(int(sys.argv[1]))
WS=[wl(S,h) for S,_ in D]
def err(T):
    hT=wl(T,h);p=np.array([cos(w,hT) for w in WS]);return np.sum((p-y)**2)
def connected(T):
    st=[s];seen={s}
    while st:
        u=st.pop()
        for v in a[u]:
            if v in T and v not in seen: seen.add(v);st.append(v)
    return len(seen)==len(T)
T=set(B(3))
bd=lambda T:list({v for u in T for v in a[u]}-T)
while len(T)<29: T.add(random.choice(bd(T)))
E=err(T);best=(E,set(T));temp=0.002
for it in range
```

```bash
cd /tmp/w && cat > cand2.py <<'EOF'
exec(open('/tmp/w/cand.py').read().split('cands={}')[0])
WS=[wl(S,3) for S,_ in D]
def err(T):
    hT=wl(T,3);p=np.array([cos(w,hT) for w in WS]);return np.sum((p-y)**2)
import itertools
C={}
for r in range(1,12):
  for name,p in list(preds.items())+[('in%d%d'%(i,j),(lambda i,j:lambda x:i<=Dg(x)<=j)(i,j)) for i in range(1,7) for j in range(i,8)]:
    T=cbfs(r,p)
    C[tuple(sorted(T))]=('cb',r,name)
    T=cbfs(99,p); C[tuple(sorted(T))]=('comp',name)
for T,n in C.items():
    if 25<=len(T)<=33: print(len(T),n,round(err(T),5))
EOF
python3 cand2.py | sort -t' 
```

```bash
cd /tmp/w && python3 - <<'EOF' | sort -k5 -g | head -30
src=open('/tmp/w/cand2.py').read()
pre=open('/tmp/w/cand.py').read()
p1=pre.split('cands={}')[0]
p2=pre.split('cands={}')[1].split('for r in range(1,9)')[0]
exec(p1+p2+src.split("split('cands={}')[0])")[1])
EOF
```

```bash
cd /tmp/w && sed -i 's/temp\*=0.9993/temp*=float(sys.argv[3])/' sa.py && time (for sd in 11 12 13 14 15 16 17 18; do python3 sa.py $sd 30000 0.99985 & done; wait)
```

```bash
cd /tmp/w && python3 -c "
import json,collections
g=json.load(open('g.json'));a=g['adj'];d=g['dist']
T=set(json.load(open('sa_18.json')))
s='b8926eb97b'
print(collections.Counter(sum(v in T for v in a[x]) for x in T))
print('start ideg',sum(v in T for v in a[s]))
for x in sorted(T,key=lambda x:d[x]): print(d[x],x,len(a[x]),sum(v in T for v in a[x]))
"
```

```bash
cd /tmp/w && cat > sa2.py <<'EOF'
exec(open('/tmp/w/sa.py').read().split('T=set(B(3))')[0])
T=set(json.load(open(sys.argv[3])))
bd=lambda T:list({v for u in T for v in a[u]}-T)
E=err(T);best=(E,set(T));temp=float(sys.argv[4])
for it in range(int(sys.argv[2])):
    T2=set(T);x=random.choice([t for t in T if t!=s]);T2.remove(x);T2.add(random.choice(bd(T2)))
    if not connected(T2): continue
    e=err(T2)
    if e<E or random.random()<math.exp((E-e)/temp): T,E=T2,e
    if E<best[0]: best=(E,set(T))
    temp*=0.9998
print(best[0])
json.dump(sorted(best[1]),open('/tmp/w/sb_%s.json'%sys.argv[1],'w'
```

```bash
cd /tmp/w && cat > cand3.py <<'EOF'
exec(open('/tmp/w/sa.py').read().split('T=set(B(3))')[0])
res=[]
for x in B(4):
    for r in range(1,6):
        T=set(ball(x,r))
        if s in T and 20<=len(T)<=40: res.append((err(T),len(T),x,r,d[x]))
        T2=T|{s}
        if s not in T and len(T2)<=40: res.append((err(T2),len(T2),x,r,d[x],'+s'))
for r in sorted(res)[:10]: print(r)
EOF
python3 cand3.py 1 0
```

```bash
cd /tmp/w && python3 -c "
import json;print('\n'.join(json.load(open('sb_5.json'))))" | probe evaluate -
```

```bash
cd /tmp/w && python3 -c "
exec(open('/tmp/w/sa.py').read().split('T=set(B(3))')[0])
T=json.load(open('sb_5.json'));hT=wl(T,3)
for S in [json.load(open('sb_1.json'))]+[json.load(open('sa_%d.json'%i)) for i in range(11,19)]:
    print(round(cos(wl(S,3),hT),4))
" 1 0
```

```bash
cd /tmp/w && python3 -c "
exec(open('/tmp/w/wl.py').read().split('if __name__')[0])
def parts(T):
    w=wl(T,3);r=[0]*4
    for (i,l),v in w.items(): r[i]+=v*v
    return r
print('ball3',parts(B(3)))
print('sb5',parts(json.load(open('sb_5.json'))))
"
```

```bash
cd /tmp/w && cat > cand4.py <<'EOF'
exec(open('/tmp/w/sa.py').read().split('T=set(B(3))')[0])
def core(S,k):
    S=set(S);ch=True
    while ch:
        ch=False
        for x in list(S):
            if sum(v in S for v in a[x])<k: S.remove(x);ch=True
    return S
def comp_of(S):
    if s not in S: return set()
    st=[s];seen={s}
    while st:
        u=st.pop()
        for v in a[u]:
            if v in S and v not in seen: seen.add(v);st.append(v)
    return seen
res=[]
for r in range(2,12):
    for k in [2,3]:
        T=comp_of(core(B(r),k))
        if T: res.append((round(err(T),5),len(T),
```

```bash
cd /tmp/w && cat >> data.py <<'EOF'
import os
if os.path.exists('/tmp/w/extra.json'):
    for S,sc in json.load(open('/tmp/w/extra.json')): D.append((S,sc))
EOF
python3 -c "
import json;json.dump([[json.load(open('/tmp/w/sb_5.json')),0.9559]],open('/tmp/w/extra.json','w'))"
cat > sa3.py <<'EOF'
exec(open('/tmp/w/wl.py').read().split('if __name__')[0])
import sys,math
h=3;random.seed(int(sys.argv[1]))
WS=[wl(S,h) for S,_ in D]
W=np.array([1+30*max(0,sc-0.85) for _,sc in D])
def err(T):
    hT=wl(T,h);nrm=sum(v*v for v in hT.values())
    p=np.array([cos(w,hT) for w in WS]);return np.sum(W*(p-y)
```

```bash
cd /tmp/w && python3 -c "
import json,glob
a=json.load(open('g.json'))['adj'];s='b8926eb97b'
for f in sorted(glob.glob('s[abc]_*.json')):
    T=set(json.load(open(f)));print(f,[v for v in a[s] if v in T])
"
```

```bash
cd /tmp/w && cat > cand5.py <<'EOF'
exec(open('/tmp/w/sa.py').read().split('T=set(B(3))')[0])
def bfs(c):
    dd={c:0};q=collections.deque([c])
    while q:
        u=q.popleft()
        for v in a[u]:
            if v not in dd: dd[v]=dd[u]+1;q.append(v)
    return dd
res=[]
for x in d:
    dx=bfs(x);L=d[x]
    T=[v for v in d if d[v]+dx[v]==L]
    if 20<=len(T)<=40: res.append((err(T),len(T),x,L))
res.sort();print(len(res));[print(r) for r in res[:10]]
EOF
python3 cand5.py 1 0
```

**agent:** The rule is "all nodes on shortest paths between the start and node 7718202434" (29 nodes), and it fits every observation. Let me confirm with an evaluate.

```bash
cd /tmp/w && cat > final.py <<'EOF'
exec(open('/tmp/w/cand5.py').read().split('res=[]')[0])
x='7718202434';dx=bfs(x)
T=[v for v in d if d[v]+dx[v]==d[x]]
open('/tmp/w/final.txt','w').write('\n'.join(T));print(len(T))
EOF
python3 final.py 1 0 && probe evaluate - < /tmp/w/final.txt
```

**agent:** Score 1.0. Submitting.

```bash
probe submit - < /tmp/w/final.txt
```

**agent:** I found the target and submitted it. It scored 1.0 on `evaluate` and the submission was accepted (29 items).

**The rule:** the target is every item that lies on some shortest path between the start item `b8926eb97b` and the item `7718202434`, which is 11 links away. That comes to 29 items.

**How I got there:**
1. **Mapping the graph.** `neighbors` was free, so I crawled everything reachable from the start: 1,599 items, with links that work both ways.
2. **Working out the score.** It isn't a plain overlap count. Selections of the same shape scored the same wherever they sat in the graph, and the start item was the only one that changed scores on its own. Small test selections with known shapes showed the score compares the structure of your selection with the target's. It does this by repeatedly labelling each item from its neighbours' labels (three rounds), with the start item labelled differently from the rest. It then compares how often each label appears. The same arithmetic showed the target has exactly 29 items and that the start links to exactly 2 of its 4 neighbours inside the target.
3. **Finding the rule.** I couldn't evaluate candidate rules directly without spending budget, so I computed offline what score each one should get on the selections I'd already tried. Balls around the start, degree-filtered regions and cores didn't fit. Search over random 29-item shapes kept returning long, thin sets, which pointed to shortest paths. "All shortest paths from the start to some item X" fit every past score almost exactly for one X, and a single `evaluate` on that set returned 1.0.

I used 109 of the 150 `evaluate` calls.

