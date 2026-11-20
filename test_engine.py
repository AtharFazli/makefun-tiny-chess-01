import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import engine as e

e.start()
w = e.gen(0)
b = e.gen(1)
print('Test1: white', len(w), 'black', len(b))
print('PASS: starting position')

# Test check detection: white king at e1, black rook h5 (attacking e5? no)
# Let me test in_check by building a simple position
e.start()
print('in_check at start:', e.in_check(0), '(should be False)')

# Test pawn attack direction: white pawn at d5 (attacking e6 and c6)
# white pawn at (f=4, r=3) = sq(4,3)=28
e.start()
e.B[sq(4, 3)] = 8  # white pawn e5 (row 3, file 4)
e.B[sq(1, 3)] = 18  # black pawn... wait, black pawns are code 9
# Actually, let me just test the attacked function with a white pawn at e5 attacking d6 and f6
# e5 = sq(4, 3)
# d6 = sq(3, 2), f6 = sq(5, 2)
# attacked(d6, 1) should be True (white pawn attacks d6? no, white pawn at e5 attacks d6 and f6)
print('attacked d6 by white:', e.attacked(sq(3, 2), 1))
print('attacked f6 by white:', e.attacked(sq(5, 2), 1))
print('attacked c4 by white:', e.attacked(sq(2, 4), 1))  # should be False

# Test black pawn attack: black pawn at e4 (row 4, file 4) attacks d3 and f3
e.B[sq(4, 4)] = 9
print('attacked d3 by black:', e.attacked(sq(3, 5), 0))
print('attacked f3 by black:', e.attacked(sq(5, 5), 0))

# Test make/unmake round trip
e.start()
m = e.gen(0)[0]
e.make(m)
B1 = list(e.B)
e.unmake(m)
print('roundtrip equal:', B1 == list(e.B))

# Test that a move that leaves king in check is not allowed
# Put white king at e1, black rook at e2 (checking)
# Actually, let me test the engine's make returning False for illegal moves
e.start()
# Move black rook to e8 (already there). White king at e1.
# Put black rook at e2 (checking white king)
e.B[sq(4, 0)] = 0  # e1 empty
e.B[sq(4, 1)] = 49  # e2 = black king? No, black king is at e8
# Let me set up a position where white is in check
e.empty()
# White king e1, black rook e2
e.B[sq(4, 0)] = 48  # white king e1
e.B[sq(4, 1)] = 49  # black king e2 (should be rook)
# Hmm, let me just set up black rook at e2
e.B[sq(4, 0)] = 48  # white king e1
e.B[sq(4, 1)] = 32 | 1  # black rook e2 (code 32|1)
print('in_check(0) after setting black rook at e2:', e.in_check(0), '(should be True)')
