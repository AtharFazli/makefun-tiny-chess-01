import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src
src.start()
s=0; tot=0
for i in range(64):
 p=src.B[i]
 if not p: continue
 t=p>>3; c=p&1
 v=[0,100,320,330,500,900][t]
 s+= (v) if c==0 else -(v)
 tot+=v
print('eval', src.evalp())
print('net material', s, 'total mat', tot, 'king', src.king, 'B[52]', src.B[52])
