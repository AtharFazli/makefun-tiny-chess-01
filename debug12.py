import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src
print('file', src.__file__)
print('after import castle=', src.castle, 'king=', src.king)
# now run start
src.start()
print('after start castle=', src.castle, 'king=', src.king)
