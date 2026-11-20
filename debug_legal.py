import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src
src.start()
print('in_check', src.in_check())
print('white king', src.ksq())
# replicate legal_moves
for side in (0, 1):
    L = []
    for m in src.gen(side):
        src.make(m)
        k = src.katt(side)
        if not k:
            L.append(m)
        src.unmake(m)
        if len(L) < 3:
            print('side', side, 'move', src.uci(m), 'katt', k)
    print('side', side, 'legal count', len(L))
