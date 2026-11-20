import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
src = open('/home/fazly/makefun/work/tiny-chess/src.py').read()
print('import line:', src.splitlines()[0])
print('json in import:', 'json' in src.splitlines()[0])
main = open('/home/fazly/makefun/work/tiny-chess/main.py','rb').read()
print('main.py has b\'import json\':', b'import json' in main)
print('main.py has b\'import lzma\':', b'import lzma' in main)
print('main.py size:', len(main))
