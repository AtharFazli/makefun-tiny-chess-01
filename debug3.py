import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src
src.start()
print('B[56]', src.B[56], 'B[4]=', src.B[4], 'B[60]=', src.B[60])
print('king', src.king)
e=src.evalp()
print('evalp', e)
# count material
tot=0
for i in range(64):
 p=src.B[i]
 if not p: continue
 t=p>>3
 if t>=0 and t<=5: tot+=1
print('non-king pieces', tot)
