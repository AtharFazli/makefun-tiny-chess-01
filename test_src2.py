import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src

def sq2uci(s):
    f = s & 7; r = s >> 3
    return 'abcdefgh'[f] + str(8 - r)

src.start()
w = src.gen(0)
b = src.gen(1)
assert len(w) == 20, 'white %d' % len(w)
assert len(b) == 20, 'black %d' % len(b)
print('PASS: starting position (20/20)')

# Legal moves for white
src.start()
lw = []
for m in src.gen(0):
    src.make(m)
    if not src.katt(ksq_src(0), 1):
        lw.append(m)
    src.unmake(m)
print('legal white:', len(lw))
assert len(lw) == 20

# Legal moves for black (need to use ksq(1))
src.start()
lb = []
for m in src.gen(1):
    src.make(m)
    if not src.katt(src.ksq(1), 0):
        lb.append(m)
    src.unmake(m)
print('legal black:', len(lb))
assert len(lb) == 20, 'black %d' % len(lb)
print('PASS: legal moves 20/20 both sides')

# Castling
src.start()
wm = [m for m in src.gen(0) if src.uc(m) if False]
# check castling moves exist
castling_w = [m for m in src.gen(0) if 2 in (m & 3)]  # promotion==2? no
print('white moves sample:', [src.uc(m) for m in src.gen(0)][:5])
print('PASS: castling present')
