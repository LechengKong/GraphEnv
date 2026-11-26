# sp-opus55-b1 / hidden-pattern-probe__3cojEj4

model=bedrock/us.anthropic.claude-opus-5-5 reward=1.0 exception=None evaluate=86 best=1.0

```bash
probe --help; probe status
```

**agent:** Let me explore the graph via BFS (free).

```bash
cd /tmp && cat > bfs.py <<'EOF'
import json,subprocess,collections
s="b8926eb97b"
adj={};dist={s:0};q=collections.deque([s])
while q:
    u=q.popleft()
    r=json.loads(subprocess.check_output(["probe","neighbors",u]))
    adj[u]=r
    if len(adj)>3000: break
    nb = r if isinstance(r,list) else r.get("neighbors",r)
    for v in nb:
        if v not in dist: dist[v]=dist[u]+1; q.append(v)
json.dump({"adj":adj,"dist":dist},open("g.json","w"))
print(len(adj),len(dist),collections.Counter(dist.values()))
print(adj[s])
EOF
python3 bfs.py
```

```bash
cd /tmp && python3 -c "
import json;g=json.load(open('g.json'));a={k:v['neighbors'] for k,v in g['adj'].items()}
asym=sum(1 for u in a for v in a[u] if u not in a[v]);print('asym',asym)
import collections;print(collections.Counter(len(v) for v in a.values()))
"
for k in 0 1 2 3; do python3 -c "
import json;g=json.load(open('/tmp/g.json'));print('\n'.join(x for x,d in g['dist'].items() if d<=$k))" | probe evaluate -; done
```

```bash
cd /tmp && for k in 4 5 6; do python3 -c "
import json;g=json.load(open('/tmp/g.json'));print('\n'.join(x for x,d in g['dist'].items() if d<=$k))" | probe evaluate -; done
```

```bash
cd /tmp && for k in 1 2 3 4 5 6; do python3 -c "
import json;g=json.load(open('/tmp/g.json'));print('\n'.join(x for x,d in g['dist'].items() if d==$k or d==0))" | probe evaluate -; done
```

```bash
cd /tmp && python3 -c "
import json;g=json.load(open('/tmp/g.json'));a={k:v['neighbors'] for k,v in g['adj'].items()}
s='b8926eb97b'
for n in a[s]: print(n,len(a[n]),a[n])
print(len(a[s]))"; for n in 40234ca2ac 7177bc61e3; do probe evaluate $n; probe evaluate b8926eb97b $n; done
```

```bash
cd /tmp && python3 -c "
import json;g=json.load(open('/tmp/g.json'))
d=g['dist']
for k in [2,3,5,10,30]:
  print([x for x in d if d[x]==k][0])" > far.txt; cat far.txt; for n in $(cat far.txt); do probe evaluate $n; done
```

```bash
cd /tmp && probe evaluate 02ac8fd827 7c68283178; probe evaluate 40234ca2ac 02ac8fd827; probe evaluate 40234ca2ac 7177bc61e3; probe evaluate 40234ca2ac 7177bc61e3 91b3c0bda3 e6f6a117af
```

```bash
cd /tmp && probe evaluate b8926eb97b 7c68283178; probe evaluate b8926eb97b 02ac8fd827;  probe evaluate b8926eb97b 3879ab56f9
```

```bash
cd /tmp && S=b8926eb97b; probe evaluate $S 40234ca2ac 7177bc61e3; probe evaluate $S 7c68283178 3879ab56f9; probe evaluate $S 40234ca2ac 7c68283178; probe evaluate $S 40234ca2ac 7177bc61e3 91b3c0bda3
```

```bash
cd /tmp && python3 -c "
import json;g=json.load(open('/tmp/g.json'));a={k:v['neighbors'] for k,v in g['adj'].items()}
for n in '7c68283178 02ac8fd827 3879ab56f9 40234ca2ac 7177bc61e3 91b3c0bda3 e6f6a117af'.split(): print(n,len(a[n]),g['dist'][n])"
```

```bash
cd /tmp && S=b8926eb97b; probe evaluate 40234ca2ac $S; probe evaluate $S $S 40234ca2ac
```

```bash
cd /tmp && python3 -c "
import json;g=json.load(open('/tmp/g.json'));d=g['dist']
b=[x for x in d if d[x]<=2]
for x in b[1:]:
  print(x,d[x],' '.join(y for y in b if y!=x))" > rem.txt; while read n dd rest; do echo "$n $dd $(probe evaluate $rest)"; done < rem.txt
```

```bash
cd /tmp && python3 -c "
import json;g=json.load(open('/tmp/g.json'));a={k:v['neighbors'] for k,v in g['adj'].items()};d=g['dist']
b=set(x for x in d if d[x]<=2)
for x in '0d66623d41 3742bb8423 f5627a7cb1 02ac8fd827 e6f6a117af 40234ca2ac aaf16439e9 91b3c0bda3 099d2ce378 58f1750432 e7a1da5fa7 7177bc61e3'.split():
  print(x,d[x],len(a[x]),sum(y in b for y in a[x]),[d[y] for y in a[x]])"
```

```bash
cd /tmp && cat > ev.py <<'EOF'
import json,sys,subprocess
g=json.load(open('/tmp/g.json'));a={k:v['neighbors'] for k,v in g['adj'].items()};d=g['dist']
def ev(S):
    S=list(dict.fromkeys(S))
    r=json.loads(subprocess.run(["probe","evaluate","-"],input="\n".join(S),capture_output=True,text=True).stdout)
    return r["score"]
EOF
python3 -c "
exec(open('/tmp/ev.py').read())
s='b8926eb97b'
B=lambda k:[x for x in d if d[x]<=k]
print('b5 deg>=4',ev([x for x in B(5) if len(a[x])>=4 or x==s]))
print('b5 deg<=4',ev([x for x in B(5) if len(a[x])<=4 or x==s]))
print('b5 + full shell6 ... b4.5: b4 + h
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
B=lambda k:[x for x in d if d[x]<=k]
print(ev(B(2)+['7c68283178']))
print(ev(B(2)+['7c68283178','bd9ff23567']))
print(ev(B(5)+['7c68283178']))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
B=lambda k:[x for x in d if d[x]<=k]
b=B(2); print(ev(b[::-1]))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
B=lambda k:[x for x in d if d[x]<=k]
fs=[x for x in d if d[x]==40][:3]
for f in fs: print(ev(B(2)+[f]))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
fs=[x for x in d if d[x]>=35]
for m in [3,6,12,25,60]: print(m,ev(['b8926eb97b']+fs[:m]))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/ev.py').read())
import collections
def ball(c,k):
  D={c:0};q=collections.deque([c])
  while q:
    u=q.popleft()
    for v in a[u]:
      if v not in D: D[v]=D[u]+1;q.append(v)
  return [x for x in D if D[x]<=k]
X=[x for x in d if d[x]==30][0]
bx=ball(X,5);print(len(bx))
print('start+ballX5',ev(['b8926eb97b']+bx[:60]))
import random;random.seed(1)
fs=[x for x in d if d[x]>=20];sc=[]
for x in random.sample(fs,len(fs)):
  if all(y not in a[x] for y in sc): sc.append(x)
  if len(sc)==60:break
print('start+60 scattered',ev(['b8926eb97b']+sc))
"
```

```bash
probe neighbors b8926eb97b; probe neighbors 40234ca2ac
```

```bash
cd /tmp && python3 -c "
import json
g=json.load(open('/tmp/g.json'))
print(set(tuple(sorted(v.keys())) for v in g['adj'].values()))"
```

```bash
probe status
```

```bash
cd /tmp && cat > data.py <<'EOF'
exec(open('/tmp/ev.py').read())
import collections,random
s='b8926eb97b'
B=lambda k:[x for x in d if d[x]<=k]
def ball(c,k):
  D={c:0};q=collections.deque([c])
  while q:
    u=q.popleft()
    for v in a[u]:
      if v not in D: D[v]=D[u]+1;q.append(v)
  return [x for x in D if D[x]<=k]
data=[]
for k,sc in zip(range(7),[.0148,.4066,.833,.9024,.8952,.9339,.9096]): data.append((B(k),sc))
for k,sc in zip(range(1,7),[.4066,.6011,.6729,.6234,.5402,.6519]): data.append(([x for x in d if d[x]==k or d[x]==0],sc))
data.append(([s,'40234ca2ac'],.3042));data.append(([s,'7
```

```bash
cd /tmp && cat > comp.py <<'EOF'
exec(open('/tmp/data.py').read())
def comp(pred):
  D={s};q=[s]
  while q:
    u=q.pop()
    for v in a[u]:
      if v not in D and pred(v): D.add(v);q.append(v)
  return list(D)
c={}
c['deg4']=comp(lambda v:len(a[v])==4)
c['deg>=4']=comp(lambda v:len(a[v])>=4)
c['deg<=4']=comp(lambda v:len(a[v])<=4)
c['deg>=3']=comp(lambda v:len(a[v])>=3)
c['deg3-4']=comp(lambda v:3<=len(a[v])<=4)
c['deg4-5']=comp(lambda v:4<=len(a[v])<=5)
for k,v in c.items(): print(k,len(v))
EOF
python3 comp.py
```

```bash
cd /tmp && cat > var.py <<'EOF'
exec(open('/tmp/data.py').read())
def sh(k): return [x for x in d if d[x]==k]
def nin(x,S): S=set(S); return sum(y in S for y in a[x])
v={}
for k in [3,4,5,6]:
  v[f'b{k-1}+sh{k}>=2']=B(k-1)+[x for x in sh(k) if nin(x,B(k-1))>=2]
v['b5-internal1']=[x for x in B(5) if nin(x,B(5))>=2 or x==s]
for k,S in v.items(): print(k,len(S),ev(S))
EOF
python3 var.py
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/comp.py').read().split('c={}')[0])
tri=sum(1 for u in a for v in a[u] for w in a[v] if w in a[u])//6
print('triangles',tri, 'edges',sum(len(x) for x in a.values())//2)
import itertools
for S in [{3},{4},{5},{3,4},{4,5},{2,3,4},{4,5,6},{3,4,5}]:
  for incl in [True]:
    c=comp(lambda v:len(a[v]) in S); print(S,len(c))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/data.py').read())
for k in [7,8]: print(k,len(B(k)),ev(B(k)))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/data.py').read())
X=[x for x in d if d[x]==30][0]
bx=[y for y in ball(X,8) if y!=s][:140]
print(len(bx),ev([s]+bx))
print(ev(B(9)), len(B(9)), len(B(10)))
"
```

```bash
cd /tmp && cat >> data.py <<'EOF'
data += [(B(7),.9249),(B(8),.9329),(B(9),.9393)]
X=[x for x in d if d[x]==30][0]
data.append(([s]+[y for y in ball(X,8) if y!=s][:140],.9218))
def feat(S):
  S=set(S);n=len(S)
  E=sum(1 for x in S for y in a[x] if y in S)//2
  bd=sum(1 for x in S for y in a[x] if y not in S)
  tri=sum(1 for u in S for v in a[u] if v in S for w in a[v] if w in S and w in a[u])//6
  return n,E,bd,tri
EOF
python3 -c "
exec(open('/tmp/data.py').read())
for S,sc in sorted(data,key=lambda t:t[1]):
  n,E,bd,tri=feat(S); print(sc,n,E,bd,tri, round(2*E/(2*E+bd),3), round(E/n,3))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/data.py').read())
print(ev(B(5)[1:]))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/data.py').read())
X=[x for x in d if d[x]==30][0]
bx=ball(X,12)[:174]; print(len(set(bx)&set(B(9))))
print(ev(bx))
"
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/data.py').read())
far=[x for x in d if d[x]>=30]
# triangle
for u in far:
  t=[(v,w) for v in a[u] for w in a[v] if w in a[u]]
  if t: tri=[u,t[0][0],t[0][1]];break
print(tri, ev(tri))
# path of 6 far nodes
p=[far[0]]
while len(p)<6:
  nx=[v for v in a[p[-1]] if v not in p and all(v not in a[q] for q in p[:-1])]
  p.append(nx[0])
print(p,ev(p))
"
```

```bash
cd /tmp && cat >> data.py <<'EOF'
data += [(B(5)[1:],.9383),(bx174:=ball(X,12)[:174],.9297)]
data += [(['7c68283178', '05dbfe13bb', '6dcdb5c81f'],.5192),(['7c68283178', '05dbfe13bb', '4b4c6525bc', 'fd3f57db84', '959990428a', '8d01fbd83d'],.6435)]
data += [([x for x in B(5) if len(a[x])>=4 or x==s],.9),([x for x in B(5) if len(a[x])<=4 or x==s],.9101)]
for k in ['40234ca2ac','7177bc61e3','91b3c0bda3','e6f6a117af','02ac8fd827','7c68283178']: data.append(([k],.4154))
data.append((['40234ca2ac','02ac8fd827'],.4154));data.append((['40234ca2ac','7177bc61e3','91b3c0bda3','e6f6a117af'],.4154))
import 
```

```bash
cd /tmp && cat > search.py <<'EOF'
exec(open('/tmp/data.py').read())
import itertools,sys
H=int(sys.argv[1])
pre=[(wl(S,H),sc) for S,sc in data]
def err(T):
  G=wl(T,H);return sum((cos(F,G)-sc)**2 for F,sc in pre)
b3=B(3);sh4=[x for x in d if d[x]==4]
best=[]
for c in itertools.combinations(sh4,3):
  T=b3+list(c);best.append((err(T),c))
best.sort();print(best[:5])
# also b3 minus k plus k+3
EOF
python3 search.py 3; python3 search.py 2
```

```bash
cd /tmp && python3 -c "
exec(open('/tmp/data.py').read())
T=B(3)+['313c79969e', 'a2a357bf60', 'd0fae90990'];G=wl(T,3)
print(sum(v*v for v in G.values()))
for S,sc in data: print(sc, round(cos(wl(S,3),G),4), len(S))
" | head -70
```

**agent:** Model pinned down: WL with 3 iterations, labels {start, normal}, global cosine; |T|=29 and start has exactly 2 neighbors inside T. Testing rule candidates offline now (no budget needed).

```bash
cd /tmp && cat > fit2.py <<'EOF'
exec(open('/tmp/data.py').read())
pre=[(wl(S,3),sc) for S,sc in data]
def err(T):
  G=wl(T,3);return max(abs(cos(F,G)-sc) for F,sc in pre)
EOF
python3 -c "
exec(open('/tmp/fit2.py').read())
for r in range(1,10):
  for name,p in [('deg4',lambda x:len(a[x])==4),('deg>=4',lambda x:len(a[x])>=4),('deg<=4',lambda x:len(a[x])<=4)]:
    T=[x for x in B(r) if p(x)]
    if 20<=len(T)<=40: print(r,name,len(T),round(err(T),4))
"
```

```bash
cd /tmp && cat > sa.py <<'EOF'
exec(open('/tmp/fit2.py').read())
import random,sys
random.seed(int(sys.argv[1]))
def sse(T):
  G=wl(T,3);return sum((cos(F,G)-sc)**2 for F,sc in pre)
U=[x for x in B(6) if x!=s]
T=set(random.sample(B(3)[1:],26)[:28]) 
while len(T)<28: T.add(random.choice(U))
cur=sse([s]+list(T));best=(cur,set(T));temp=0.01
for it in range(20000):
  # move: swap, prefer nodes adjacent to T
  out=random.choice(list(T))
  cand=[y for x in list(T)+[s] for y in a[x] if y not in T and y!=s]
  inn=random.choice(cand) if random.random()<0.9 else random.choice(U)
  if inn in T: continue

```

```bash
cd /tmp && sed -i 's/T=set(random.sample(B(3)\[1:\],26)\[:28\]) /T=set(B(3)[1:])/' sa.py && (for i in 1 2 3 4; do timeout 550 python3 sa.py $i & done; wait)
```

```bash
cd /tmp && cat > show.py <<'EOF'
exec(open('/tmp/data.py').read())
import sys
for line in sys.stdin:
  T=line.split()
  if len(T)<5: continue
  n,E,bd,tri=feat(T);Ts=set(T)
  print(n,E,tri,sorted(collections.Counter(sum(y in Ts for y in a[x]) for x in T).items()), sorted(collections.Counter(d[x] for x in T).items()))
  # components
  seen=set();cs=[]
  for x in T:
    if x in seen: continue
    st=[x];seen.add(x);c=0
    while st:
      u=st.pop();c+=1
      for v in a[u]:
        if v in Ts and v not in seen: seen.add(v);st.append(v)
    cs.append(c)
  print(' comps',cs)
EOF
python3 show.py <
```

```bash
cd /tmp && probe status && python3 - <<'EOF'
exec(open('/tmp/data.py').read())
json.dump([[list(S),sc] for S,sc in data],open('/tmp/dat.json','w'))
EOF
cat > sa2.py <<'EOF'
import json,math,random,sys,collections
g=json.load(open('/tmp/g.json'));a={k:v['neighbors'] for k,v in g['adj'].items()};d=g['dist']
s='b8926eb97b'
def wl(S,H=3):
  S=set(S);lab={x:('S' if x==s else 'N') for x in S};F=collections.Counter()
  for x in S:F[(0,lab[x])]+=1
  for h in range(1,H+1):
    lab={x:hash((lab[x],tuple(sorted(lab[y] for y in a[x] if y in S)))) for x in S}
    for x in S:F[(h,lab[x])]+=1
  return F
def 
```

```bash
cd /tmp && (for i in 1 2 3 4 5 6 7 8; do python3 sa2.py $i 30000 > fit_$i.json & done; wait); for i in 1 2 3 4 5 6 7 8; do python3 -c "import json;r=json.load(open('/tmp/fit_$i.json'));print(r['e'],r['max'])"; done
```

```bash
cd /tmp && cat > addev.py <<'EOF'
import json,subprocess,sys
data=json.load(open('/tmp/dat.json'))
for f in sys.argv[1:]:
  T=json.load(open(f))['T']
  r=json.loads(subprocess.run(["probe","evaluate","-"],input="\n".join(T),capture_output=True,text=True).stdout)
  print(f,r);data.append([T,r['score']])
json.dump(data,open('/tmp/dat.json','w'))
EOF
python3 addev.py fit_8.json fit_2.json
```

```bash
cd /tmp && for round in 1 2 3; do (for i in 1 2 3 4 5 6 7 8; do python3 sa2.py $((i+round*10)) 30000 > fit_$i.json & done; wait); best=$(for i in 1 2 3 4 5 6 7 8; do python3 -c "import json;r=json.load(open('/tmp/fit_$i.json'));print(r['e'],'fit_$i.json')"; done | sort -g | head -2 | awk '{print $2}'); python3 addev.py $best; done
```

```bash
cd /tmp && cat > fam.py <<'EOF'
exec(open('/tmp/sa2.py').read().split('random.seed')[0])
def bfs(src,allowed=None):
  D={src:0};q=collections.deque([src])
  while q:
    u=q.popleft()
    for v in a[u]:
      if v not in D and (allowed is None or v in allowed): D[v]=D[u]+1;q.append(v)
  return D
def mx(T):
  G=wl(T);return max(abs(cos(F,G)-sc) for F,sc,n in pre)
res=[]
ds=bfs(s)
# shortest path unions
for X in d:
  if d[X]>14: continue
  dx=bfs(X)
  T=[y for y in ds if ds[y]+dx.get(y,99)==ds[X]]
  if s in T and 15<=len(T)<=45: res.append((mx(T),'sp',X,len(T)))
  # nodes with ds+dx <= L+slack
 
```

**agent:** Found it: the union of all shortest paths from the start to item `7718202434` has 29 items and reproduces all ~70 observed scores to rounding precision. Confirming with one evaluate:

```bash
cd /tmp && python3 - <<'EOF' > final.txt
exec(open('/tmp/fam.py').read().split('res=[]')[0])
ds=bfs(s);X='7718202434';dx=bfs(X)
print("\n".join(y for y in ds if ds[y]+dx.get(y,99)==ds[X]))
EOF
wc -l final.txt; probe evaluate - < final.txt
```

**agent:** Score 1.0. Submitting.

```bash
probe submit - < /tmp/final.txt
```

**agent:** I submitted a 29-item selection that scored 1.0 on `evaluate`, and it was accepted. I used 86 of the 150 evaluate calls.

**The rule:** the target is every item that lies on a shortest path between the start item `b8926eb97b` and item `7718202434`, which is 14 links away.

**How I found it:**
1. I mapped the whole system for free with `neighbors`: 1,599 items, all reachable from the start, with links that go both ways.
2. The scores didn't act like a simple overlap measure. A cluster of items far from the start scored almost as high as the area around the start (about 0.93 vs 0.94). That meant the score depends mostly on the *shape* of the links inside the selection, not on which items are in it.
3. I narrowed it down to a specific formula: it compares the link patterns around each item, three steps out, with the start item marked as special. This matched my small test selections to four decimal places. Those tests showed the target has 29 items and that the start is linked to exactly two of them.
4. A start with only two links inside the target pointed away from the obvious "everything within N links" rule. None of those (distance 1 to 9) scored 1.0 anyway. I then checked other candidate rules offline against all the scores I'd collected. The shortest-path rule to `7718202434` reproduced every observed score to within rounding, and no other candidate came close (next best was off by about 0.02).
5. One `evaluate` on that set returned 1.0, and I submitted it.

Because the score depends on shape, a different set with exactly the same link pattern could in principle also score 1.0. That doesn't affect this result.

