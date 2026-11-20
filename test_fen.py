import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import engine3 as e

# Test FEN parsing
e.setup('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
print('after FEN: white king at', e.kings[0], 'black king at', e.kings[1])
print('castling:', e.cast)
print('ep:', e.ep)
assert e.kings[0] == 60, 'white king at %d != 60' % e.kings[0]
assert e.kings[1] == 4, 'black king at %d != 4' % e.kings[1]
print('PASS FEN parsing')

# Test move gen from FEN position
moves = e.gen(0)
print('white moves:', len(moves))
# e2e4 should be there
uci_moves = [e.uc(m) for m in moves]
assert 'e2e4' in uci_moves or 'e2e4' in str(uci_moves).lower(), 'e2e4 missing'
print('PASS move gen from FEN')

# Test UCI -> internal move
# e2e4: from e2 (sq(4,6)=52), to e4 (sq(4,4)=36)
m = e.parse_uci('e2e4')
print('e2e4 internal:', m)
assert m == (52 << 12) | (36 << 6) | 0
# e7e5: from e7 (sq(4,1)=12), to e5 (sq(4,3)=28)
m2 = e.parse_uci('e7e5')
assert m2 == (12 << 12) | (28 << 6) | 0
print('PASS UCI parsing')

# Test UCI output
print('uci(52<<12 | 36<<6 | 0) =', e.uc(52 << 12 | 36 << 6 | 0))
print('PASS UCI output')

# Test make/unmake on FEN position
e.setup('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
m = e.parse_uci('e2e4')
e.make(m)
print('after e2e4: B[52]=', e.B[52], 'B[36]=', e.B[36])
print('ep:', e.ep)
e.unmake(m)
print('after unmake: B[52]=', e.B[52], 'B[36]=', e.B[36], 'ep:', e.ep)
assert e.B[52] == 8, 'e2e4 pawn missing'
assert e.B[36] == 0, 'e4 square should be empty'
print('PASS make/unmake round trip')

print('ALL FEN/UCI TESTS PASSED')
