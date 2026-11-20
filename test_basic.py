import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src
src.start()
w = src.gen(0)
b = src.gen(1)
print('white', len(w), 'black', len(b))
assert len(w) == 20, 'white %d != 20' % len(w)
assert len(b) == 20, 'black %d != 20' % len(b)
# legality check
src.start()
legal_w = []
for m in src.gen(0):
    src.make(m)
    legal_w.append(src.in_check(0) == 0)
    src.unmake(m)
print('legal white', sum(legal_w))
assert sum(legal_w) == 20
src.start()
legal_b = []
for m in src.gen(1):
    src.make(m)
    legal_b.append(src.in_check(1) == 0)
    src.unmake(m)
print('legal black', sum(legal_b))
assert sum(legal_b) == 20
# evaluate
import src as e
print('evaluate start:', e.evalp())
print('in_check:', e.in_check(0), e.in_check(1))
# test UCI round trip
m2 = e.parse_uci('e2e4')
print('e2e4:', e.uc(m2), m2)
src.start()
src.make(m2)
print('after e2e4 king0:', e.king[0], 'ep:', e.ep)
src.unmake(m2)
print('OK')
