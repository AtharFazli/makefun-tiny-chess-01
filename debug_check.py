import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import engine3 as e

e.start()
e.B[e.sq(4, 6)] = 32 | 1
print('B[52] (e2):', e.B[52])
print('white king sq:', e.kings[0], 'B[60]:', e.B[60])
print('attacked(60, 1):', e.attacked(60, 1))
# also check the sliding loop manually
print('rook moves from e2:')
for d in (1, 8, -1, -8, 7, 9, -7, -9):
    q = 52 + d
    while 0 <= q < 64 and not e.B[q]:
        q += d
    print('  d=%d q=%d B[q]=%d' % (d, q, e.B[q] if 0 <= q < 64 else 'out'))
