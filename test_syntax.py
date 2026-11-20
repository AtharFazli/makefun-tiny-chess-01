import ast
src = open('/home/fazly/makefun/work/tiny-chess/src.py').read()
ast.parse(src)
print('syntax ok')
