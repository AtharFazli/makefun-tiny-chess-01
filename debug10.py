import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src
print(type(src.start), src.start)
import inspect
print(inspect.getsource(src.start))
print('castle in module', src.castle)
print('calling empty')
src.empty()
print('after empty castle', src.castle, 'king', src.king)
