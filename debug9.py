import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src
src.castle=15
print('after direct castle:', src.castle)
src.start()
print('after start:', src.castle, src.king)
