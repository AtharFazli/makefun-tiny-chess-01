import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src

# Test make/unmake round trip with en passant
src.setup('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
e2e4 = src.parse_uci('e2e4')
src.make(e2e4)
print('after e2e4: B[52]=', src.B[52], 'B[36]=', src.B[36], 'ep=', src.ep)
src.unmake(e2e4)
print('after unmake: B[52]=', src.B[52], 'B[36]=', src.B[36], 'ep=', src.ep)
assert src.B[52] == 8, 'pawn missing'
assert src.B[36] == 0, 'e4 should be empty'
print('PASS: round trip')

# Test FEN parsing
src.setup('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
print('white king:', src.kings[0], 'black king:', src.kings[1])
assert src.kings[0] == 60
assert src.kings[1] == 4
print('PASS: kings')

# Test legal moves
moves = src.gen(0)
assert len(moves) == 20
print('PASS: 20 moves')

# Test UCI parsing
m = src.parse_uci('e2e4')
assert m == (52 << 12) | (36 << 6) | 0
print('PASS: UCI parse')

print('ALL TESTS PASSED')
