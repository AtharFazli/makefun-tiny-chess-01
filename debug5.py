import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src
print('sq(4,7)=', src.sq(4,7), 'sq(4,0)=', src.sq(4,0))
src.start()
print('after start king =', src.king)
# force
src.king=[60,4]
print('forced', src.king)
