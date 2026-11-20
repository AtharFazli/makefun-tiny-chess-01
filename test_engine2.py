import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import engine as e

def sq2uci(s):
    f = s & 7
    r = s >> 3
    return 'abcdefgh'[f] + str(8 - r)

e.start()
w = e.gen(0)
b = e.gen(1)
print('Test1: white', len(w), 'black', len(b))
assert len(w) == 20, 'white should have 20'
assert len(b) == 20, 'black should have 20'
print('PASS: starting position')

print('Check at start:', e.in_check(0), '(should be False)')
print('Check black at start:', e.in_check(1), '(should be False)')

# Test pawn attack direction
e.start()
# white pawn e5 (row 3, file 4) attacks d6 and f6
print('white pawn attacks d6:', e.attacked(sq(3, 2), 1))
print('white pawn attacks f6:', e.attacked(sq(5, 2), 1))
# black pawn e4 (row 4, file 4) attacks d3 and f3
e.B[sq(4, 4)] = 9
print('black pawn attacks d3:', e.attacked(sq(3, 5), 0))
print('black pawn attacks f3:', e.attacked(sq(5, 5), 0))

# Test make/unmake round trip
e.start()
m = e.gen(0)[0]
e.make(m)
B1 = list(e.B)
e.unmake(m)
print('roundtrip equal:', B1 == list(e.B))

# Test illegal move (leaves king in check)
e.start()
# Move black rook to e2 (checking white king at e1)
e.B[sq(4, 0)] = 0  # e1 empty... wait, white king is at e1
# Let me reposition
e.B[sq(4, 7)] = 48  # white king e8? no, row 7 = rank 1
# White king at e1 = sq(4, 7) in this convention
# Actually kings were set by start(): kings[0] = sq(4,7), kings[1] = sq(4,0)
# White king at sq(4,7)=60 (row 7, file 4)
# Put black rook at e2 = sq(4, 1) = 12? No, sq(4,1) = 1*8+4 = 12
e.B[sq(4, 1)] = 32 | 1  # black rook at e2 (row 1)
print('in_check after black rook at e2:', e.in_check(0), '(should be True)')
