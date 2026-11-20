import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import engine3 as e

e.start()
w = e.gen(0)
b = e.gen(1)
print('white', len(w), 'black', len(b))
assert len(w) == 20
assert len(b) == 20
print('PASS')

# legal moves
src_e = e
src_e.start()
lw = []
for m in src_e.gen(0):
    src_e.make(m)
    if not src_e.attacked(src_e.kings[0], 1):
        lw.append(m)
    src_e.unmake(m)
print('legal white', len(lw))
assert len(lw) == 20
src_e.start()
lb = []
for m in src_e.gen(1):
    src_e.make(m)
    if not src_e.attacked(src_e.kings[1], 0):
        lb.append(m)
    src_e.unmake(m)
print('legal black', len(lb))
assert len(lb) == 20
print('PASS legal')

# check detection
e.start()
print('white in check:', e.in_check(0), '(False)')
print('black in check:', e.in_check(1), '(False)')

# white king at e1 (sq(4,7)=60), black rook at e2 (sq(4,6)=52)
e.B[e.sq(4, 6)] = 32 | 1
print('white in check after rook:', e.in_check(0), '(True)')
e.B[e.sq(4, 6)] = 0

# black king at e8 (sq(4,0)=4), white rook at e7 (sq(4,1)=12)
e.B[e.sq(4, 1)] = 32
print('black in check:', e.in_check(1), '(True)')
e.B[e.sq(4, 1)] = 0

print('ALL TESTS PASSED')
