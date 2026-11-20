import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src
# emulate start
src.empty()
back=(32,16,24,40,48,24,16,32)
for i in range(8):
    src.B[src.sq(i,7)]=back[i]
    src.B[src.sq(i,0)]=back[i]|1
for f in range(8):
    src.B[src.sq(f,6)]=8
    src.B[src.sq(f,1)]=9
src.castle=15
src.king=[src.sq(4,7),src.sq(4,0)]
print('after emulate king =', src.king, 'castle', src.castle)
