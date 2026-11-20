import importlib.util
spec=importlib.util.spec_from_file_location('src','/home/fazly/makefun/work/tiny-chess/src.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.start()
L=m.gen(0)
print('legal moves:', len(L))
m.setup('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
m.start()
moves=m.gen(0)
print('start legal:', len(moves))
print('sample choose:', m.uc(moves[0]) if moves else 'none')
import random
for g in range(10):
    moves=m.gen(0)
    mm=random.choice(moves)
    m.make(mm)
    m.unmake(mm)
print('SANITY OK')
