import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src
print('module start at', src.start.__code__.co_firstlineno)
src.start()
print('after start:', src.castle, src.king)
import inspect
src2 = inspect.getsource(src.start)
print(src2)
