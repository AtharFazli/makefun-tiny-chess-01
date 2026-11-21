import lzma,os,sys,json,urllib.request as U,urllib.error as E,random
MT=[0,100,320,330,500,900]
PA=[0,0,20,34,38,40,34,0]
PF=[0,10,15,21,21,15,10,0]
BS=8
B=[0]*64
castle=0
ep=-1
epk=-1
king=[-1,-1]
hist=[0]*8192
kil=[-1,-1]
TH=[0]*2048
TM=[0]*2048
TF=[0]*2048
TV=[0]*2048
TD=[0]*2048
SZ=16384
zn=[]
def sq(f,r):return r*8+f
def tk(p):return p>>3
def cl(p):return p&1
def st(s):return s//8
def ft(s):return s%8
def hinit():
 global zn
 rn=random.Random(7)
 zn=[rn.getrandbits(31) for _ in range(SZ)]
def zone():return zn
hinit()
def empty():
 global B,castle,ep,epk,king,hist,kil,TH,TMP,TF,TV,TDL
 B=[0]*64;castle=0;ep=-1;epk=-1;king=[-1,-1];hist=[0]*8192;kil=[-1,-1]
 TH=[0]*2048;TMP=[0]*2048;TF=[0]*2048;TV=[0]*2048;TDL=[0]*2048
def start():
 global B,castle,ep,epk,king,hist,kil
 empty()
 back=(32,16,24,40,48,24,16,32)
 for i in range(8):
  B[sq(i,7)]=back[i];B[sq(i,0)]=back[i]|1
 for f in range(8):
  B[sq(f,6)]=8;B[sq(f,1)]=9
 castle=15;king=[sq(4,7),sq(4,0)]
def setup(fen):
 global B,castle,ep,epk,king
 empty()
 p=fen.split();r=p[0].split('/')
 for rr in range(8):
  f=0
  for ch in r[rr]:
   if ch.isdigit():f+=int(ch);continue
   c=ch.lower();t='pnbrqk'.find(c)+1;col=0 if ch.isupper() else 1
   B[sq(f,rr)]=(t<<3)|col;f+=1
 castle=0
 for ch in p[2]:
  if ch in 'KQkq':castle|=1<<'KQkq'.find(ch)
 if p[3]!='-':ep=sq('abcdefgh'.find(p[3][0]),7-int(p[3][1]))
 for s in range(64):
  if B[s] and tk(B[s])==6:king[cl(B[s])]=s
def attacked(s,by):
 if not(0<=s<64)or not B[s]:return False
 for d in(17,15,10,6,-17,-15,-10,-6):
  q=s+d
  if 0<=q<64 and B[q] and tk(B[q])==2 and cl(B[q])==by:return True
 code=8 if by==0 else 9
 if by==0:
  if(s%8<7 and s>=7 and B[s-7]==code)or(s%8>0 and s>=9 and B[s-9]==code):return True
 else:
  if(s%8<7 and s+7<64 and B[s+7]==code)or(s%8>0 and s+9<64 and B[s+9]==code):return True
 for d in(1,8,-1,-8):
  q=s+d
  while 0<=q<64 and not B[q]:q+=d
  if 0<=q<64 and B[q] and cl(B[q])==by and tk(B[q])in(4,5):return True
 for d in(7,9,-7,-9):
  q=s+d
  while 0<=q<64 and not B[q]:q+=d
  if 0<=q<64 and B[q] and cl(B[q])==by and tk(B[q])in(3,5):return True
 return False
def in_check(side):return king[side]>=0 and attacked(king[side],side^1)
def gen(side):
 L=[]
 for s in range(64):
  p=B[s]
  if not p:continue
  t=tk(p);c=cl(p)
  if c!=side:continue
  if t==1:
   d=-8 if side==0 else 8
   if 0<=s+d<64 and not B[s+d]:
    if(st(s)==(6 if side==0 else 1) and not B[s+2*d]):L.append((s<<12)|((s+2*d)<<6)|2)
    L.append((s<<12)|((s+d)<<6)|0)
   for ds in((-9,7) if side==0 else(7,9)):
    q=s+ds
    if 0<=q<64 and abs(q%8-s%8)==1 and B[q] and cl(B[q])!=c:L.append((s<<12)|(q<<6)|0)
   if ep>=0 and st(s)in(3,4):
    if ep==s-7 and s%8<7 and B[s+1]==9:L.append((s<<12)|(ep<<6)|0)
    if ep==s-9 and s%8>0 and B[s-1]==9:L.append((s<<12)|(ep<<6)|0)
  elif t==2:
   for d in(17,15,10,6,-17,-15,-10,-6):
    q=s+d
    if 0<=q<64 and abs(q%8-s%8)<=2 and(not B[q] or cl(B[q])!=c):L.append((s<<12)|(q<<6)|0)
  elif t==3:
   for d in(7,9,-7,-9):
    q=s+d
    while 0<=q<64:
     qv=B[q]
     if not qv:break
     if cl(qv)!=c and tk(qv)==3:L.append((s<<12)|(q<<6)|0)
     elif cl(qv)==c:break
     q+=d
  elif t==4:
   for d in(1,8,-1,-8):
    q=s+d
    while 0<=q<64:
     qv=B[q]
     if not qv:break
     if cl(qv)!=c and tk(qv)==4:L.append((s<<12)|(q<<6)|0)
     elif cl(qv)==c:break
     q+=d
  elif t==5:
   for d in(1,8,-1,-8,7,9,-7,-9):
    q=s+d
    while 0<=q<64:
     qv=B[q]
     if not qv:break
     if cl(qv)!=c and tk(qv)==5:L.append((s<<12)|(q<<6)|0)
     elif cl(qv)==c:break
     q+=d
  elif t==6:
   for d in(1,8,-1,-8,7,9,-7,-9):
    q=s+d
    if 0<=q<64 and(not B[q] or cl(B[q])!=c):L.append((s<<12)|(q<<6)|0)
   if c==0:
    if castle&1 and not B[sq(5,7)] and not B[sq(6,7)] and not in_check(0):L.append((sq(4,7)<<12)|(sq(6,7)<<6)|0)
    if castle&2 and not B[sq(3,7)] and not B[sq(2,7)] and not in_check(0):L.append((sq(4,7)<<12)|(sq(2,7)<<6)|0)
   else:
    if castle&4 and not B[sq(5,0)] and not B[sq(6,0)] and not in_check(1):L.append((sq(4,0)<<12)|(sq(6,0)<<6)|0)
    if castle&8 and not B[sq(3,0)] and not B[sq(2,0)] and not in_check(1):L.append((sq(4,0)<<12)|(sq(2,0)<<6)|0)
 return L
def is_legal(side,m):
 f=m>>12;t=m>>6&63;p=B[f];c=cl(p);t0=tk(p)
 if t0==1:
  if t-f==16 or f-t==16:return True
  if t==f+8 and not B[t]:return False
  if t==f-8 and not B[t]:return False
  if epk>=0 and t==epk:return False
  return True
 if t0==6:
  if castle&1 and f==sq(4,7) and not B[sq(5,7)] and not B[sq(6,7)] and not attacked(sq(6,7),0):return sq(6,7)==t
  if castle&2 and f==sq(4,7) and not B[sq(3,7)] and not B[sq(2,7)] and not attacked(sq(2,7),0):return sq(2,7)==t
  if castle&4 and f==sq(4,0) and not B[sq(5,0)] and not B[sq(6,0)] and not attacked(sq(6,0),1):return sq(6,0)==t
  if castle&8 and f==sq(4,0) and not B[sq(3,0)] and not B[sq(2,0)] and not attacked(sq(2,0),1):return sq(2,0)==t
  return False
 if t0==4:
  if f==sq(4,7) or f==sq(4,0):return False
  return True
 return True
def make(m):
 global B,castle,ep,epk,king,hist,kil
 f=m>>12;t=m>>6&63;pr=m&3;p=B[f];c=cl(p);t0=tk(p)
 epk=ep;ep=-1
 B[f]=0;B[t]=p
 if t0==1:
  if t-f==16:ep=f+8
  elif f-t==16:ep=f-8
  else:
   ep=-1
   if epk>=0 and t==epk:epk=(t+8)if c==0 else(t-8)
 if t0==6:
  king[c]=t
 elif t0==4:
  if f==sq(7,7)or f==sq(0,7):king[1]=t
  if f==sq(7,0)or f==sq(0,0):king[0]=t
 if t0==6:
  if c==0:castle&=12
  else:castle&=3
 elif t0==4:
  if f==sq(7,7):castle&=254
  if f==sq(0,7):castle&=253
  if f==sq(7,0):castle&=251
  if f==sq(0,0):castle&=247
def unmake(m):
 global B,castle,ep,epk,king,hist,kil
 f=m>>12;t=m>>6&63;pr=m&3;p=B[t];c=cl(p);t0=tk(p)
 B[t]=0;B[f]=p
 if epk>=0:B[epk]=0
 if t0==6:
  king[c]=f
  if c==0:castle|=12
  else:castle|=3
 elif t0==4:
  if f==sq(7,7):castle|=1
  if f==sq(0,7):castle|=2
  if f==sq(7,0):castle|=4
  if f==sq(0,0):castle|=8
 ep=epk
def uc(m):
 f1=m>>12;r1=f1>>3;f2=m>>6&63;r2=f2>>3
 s='abcdefgh'[f1&7]+str(8-r1)+'abcdefgh'[f2&7]+str(8-r2)
 return s if m&3==0 else s+'pnbrq'[m&3]
def parse_uci(uci):
 f1='abcdefgh'.find(uci[0]);r1=8-int(uci[1])
 f2='abcdefgh'.find(uci[2]);r2=8-int(uci[3])
 pr='pnbrq'.find(uci[4]) if len(uci)>4 else 0
 return(sq(f1,r1)<<12)|(sq(f2,r2)<<6)|pr
def evalp(s):
 s0=0
 for i in range(64):
  p=B[i]
  if not p:continue
  t=tk(p);c=cl(p)
  if t==6:continue
  v=MT[t];r=i>>3;f=i&7
  if c==1:r=7-r;f=7-f
  if t==1:s0+=(v+PA[r]+PF[f])if c==0 else-(v+PA[r]+PF[f])
  elif t==2:s0+=(v+5*(7-abs(r-3)-abs(f-3)))if c==0 else-(v+5*(7-abs(r-3)-abs(f-3)))
  elif t==3:s0+=(v+5*(7-abs(r-3)-abs(f-3)))if c==0 else-(v+5*(7-abs(r-3)-abs(f-3)))
  elif t==4:s0+=(v+5*(7-abs(r-3)-abs(f-3))+3*(r==6 or r==1))if c==0 else-(v+5*(7-abs(r-3)-abs(f-3))+3*(r==1 or r==6))
  elif t==5:s0+=(v+3*(7-abs(r-3)-abs(f-3)))if c==0 else-(v+3*(7-abs(r-3)-abs(f-3)))
 wk=king[0];bk=king[1]
 if wk>=0:s0+=80-12*(7-(wk>>3))
 if bk>=0:s0+=12*(bk>>3)-80
 if wk>=0 and (wk&7==0 or wk&7==7):s0+=15
 if bk>=0 and (bk&7==0 or bk&7==7):s0-=15
 for i in range(64):
  p=B[i]
  if not p:continue
  if tk(p)!=1:continue
  c=cl(p);r=i>>3
  if c==0 and r>1 and not B[i-8] and not B[i-16]:s0+=8
  if c==1 and r<6 and not B[i+8] and not B[i+16]:s0-=8
 static=s0
 if s==1:s0=-static
 s0+=8*len(gen(s))
 return s0
def hashf():
 h=0
 for i in range(64):
  if B[i]:h^=zn[(tk(B[i])<<1)|cl(B[i])|i*128]
 if castle:h^=zn[128+castle]
 if ep>=0:h^=zn[192+ep]
 return h
N0=[0];LIMIT=15000
def node_lim():
 N0[0]+=1
 if N0[0]>LIMIT:return True
 return False
def quiesce(s,a,b):
 if node_lim():return a
 sc=evalp(s)
 if sc>=b:return b
 if sc>a:a=sc
 for m in gen(s):
  make(m)
  sc=-quiesce(s^1,-b,-a)
  unmake(m)
  if sc>=b:return b
  if sc>a:a=sc
 return a
def search(s,d,af,bf):
 global TV,TF
 if d<=0:return quiesce(s,af,bf)
 if node_lim():return af
 h=hashf()%2048
 if TF[h]:
  v=TV[h]
  if TF[h]==1 and v>=bf:return v
  if TF[h]==2 and v<=af:return v
  if TF[h]==3:return v
  if TF[h]==1 and v>af:af=v
  if TF[h]==2 and v<bf:bf=v
 mv=TM[h]
 cand=[]
 if mv:
  f=mv>>12;t=mv>>6&63;p=B[f]
  if B[t] and p and 1 <= (p>>3) <= 5:cand.append(mv)
 for m in gen(s):
  if m!=mv:cand.append(m)
 if not cand:cand=gen(s)
 if not cand:return 0
 best=af-1;best_m=None
 pk=kil[0];nk=kil[1]
 ordered=[]
 captures=[]
 quiets=[]
 for m in cand:
  f_sq=m>>12
  fp=B[f_sq]
  t=(B[(m>>6)&63])>>3
  if t==6 or fp==0 or (fp>>3)==6:continue
  if B[(m>>6)&63]:
   captures.append(m)
  else:
   quiets.append(m)
 captures.sort(key=lambda m:(MT[tk(B[(m>>6)&63])]-MT[tk(B[(m>>12)])],m),reverse=True)
 for m in quiets:
  if m==pk:kil[0]=nk;kil[1]=pk;continue
 quiets.sort(key=lambda m:hist[m>>12],reverse=True)
 for m in captures:
  if m not in ordered:ordered.append(m)
 ordered+=quiets
 if kil[0]>=0:ordered.insert(0,kil[0])
 if kil[1]>=0:ordered.insert(1,kil[1])
 for m in ordered:
  make(m)
  sc=-search(s^1,d-1,-bf,-af)
  unmake(m)
  if sc>af:
   af=sc
   if sc>=bf:return sc
   if sc>best:best=sc;best_m=m
  if af>=bf:break
 if best<af:TV[h]=af;TF[h]=2
 elif best>af:TV[h]=best;TF[h]=1
 TM[h]=best_m
 return af
def choose(fen,legal):
 setup(fen)
 s=0
 g=fen.split()
 if len(g)>1 and g[1]=='b':s=1
 best=None;bs=-100001
 BUDGET=50000;MAXD=20;N0[0]=0
 global LIMIT
 for depth in range(1,MAXD+1):
  LIMIT=BUDGET
  bm=None;bv=-100000
  for m in legal:
   mi=parse_uci(m)
   if not is_legal(s,mi):continue
   make(mi)
   sc=search(s,depth-1,-100000,100000)
   unmake(mi)
   if sc>bv:bv=sc;bm=mi
  if bm is not None and bv>bs:
   bs=bv;best=bm;BMV=bm
  if node_lim():break
 return uc(best) if best else legal[0]
def post(p,b):
 req=U.Request(ENV_URL+p,data=json.dumps(b).encode(),headers={'content-type':'application/json'})
 try:
  with U.urlopen(req) as r:return json.load(r)
 except E.HTTPError as e:sys.exit('HTTP%d:%s'%(e.code,e.read().decode(errors='replace')))
def main():
 global ENV_URL
 ENV_URL=os.environ.get('MAKEFUN_ENV_URL') or sys.exit('MAKEFUN_ENV_URL not set')
 while 1:
  g=post('/game',{})
  if g.get('status')=='done':break
  while g.get('status')=='your_move':
   L=g.get('legal_moves',[])
   if not L:sys.exit('no legal')
   g=post('/move',{'game':g.get('game'),'move':choose(g.get('fen',''),L)})
if __name__=='__main__':main()
