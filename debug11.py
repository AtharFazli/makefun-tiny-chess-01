import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src
print('after import castle=', src.castle, 'king=', src.king)
import inspect
src.start()
print('after start castle=', src.castle, 'king=', src.king)
print('module-level castle line =', repr(inspect.getsource(src.start).split('\n')[-1]))
