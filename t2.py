import sys
sys.path.insert(0,'/home/fazly/makefun/work/tiny-chess')
import src
src.start()
print('B[56]=',src.getv(src.sq(0,7)),'B[57]=',src.getv(src.sq(1,7)),'B[58]=',src.getv(src.sq(2,7)))
print('B[32]=',src.getv(src.sq(4,0)),'B[33]=',src.getv(src.sq(5,0)),'B[60]=',src.getv(src.sq(4,7)))
print('B[48]=',src.getv(src.sq(0,6)),'B[8]=',src.getv(src.sq(0,1)))
print('gen0',len(src.gen(0)),'gen1',len(src.gen(1)))
print('white:',[src.uci(m) for m in src.gen(0)][:30])
