import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src
src.start()
print('B[0]', src.B[0], 'B[4]', src.B[4], 'B[52]', src.B[52])
print('king', src.king)
print('eval', src.evalp())
# manual sum
s=0
for i in range(64):
 p=src.B[i]
 if not p: continue
 t=p>>3; c=p&1
 if t==6: continue
 v=[0,100,320,330,500,900][t]
 s+= (v) if c==0 else -(v)
print('manual material', s)
