import sys
sys.path.insert(0,'/home/fazly/makefun/work/tiny-chess')
import src
src.start()
for f in range(8):
    print('file',f,'e1',src.getv(src.sq(4,7)),'a1',src.getv(src.sq(0,7)),'h1',src.getv(src.sq(7,7)),'r2pawn',src.getv(src.sq(f,6)),'r7pawn',src.getv(src.sq(f,1)))
print('gen0 count', len(src.gen(0)))
g0=src.gen(0)
print('gen0 sample', [src.uci(g0[i]) for i in range(min(24,len(g0)))])
