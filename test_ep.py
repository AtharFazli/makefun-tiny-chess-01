import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import engine as e

# Test 1: starting position - white 20, black 20
e.start()
w = e.gen(0)
b = e.gen(1)
print('Test1: white', len(w), 'black', len(b))
assert len(w) == 20, 'white should have 20'
assert len(b) == 20, 'black should have 20'

# Test 2: e4 e5 2. Nf3 (standard opening)
e.start()
e.setup('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
# manually: white e2e4, black e7e5, white g1f3
# Instead test gen directly after setup
# Let's test castling
w_mv = e.gen(0)
print('Test2: white moves count', len(w_mv))
# castling should be in there

# Test 3: en passant
# Set up: white pawn e5 (row 4, file 4), black pawn d5 (row 4, file 3) just double-pushed?
# Actually set up: black pawn d5 (row 3? no)
# Let's build carefully.
e.setup('rnbqkbnr/ppp1pppp/8/8/3Pp3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1')
# Black pawn d5, white pawn e5, white to move, can capture en passant with exd6?
# In this FEN, ep square would be... white pawn e5 (row 4, file 4), black pawn d5 (row 4, file 3).
# Black just double-pushed from d7 to d5? No, black pawns start row 1.
# Wait, the FEN has black pawns at row 1 (rank 7)? No, the FEN is standard.
# Actually, in the FEN, the rows are: rank 8 (row 0), rank 7 (row 1), ..., rank 1 (row 7).
# FEN '3Pp3': rank 5 = three empty, P (white pawn), p (black pawn), three empty.
# So rank 5: file d = white pawn P, file e = black pawn p? Wait, '3Pp3' = 3 empty, then P (white at file d), then p (black at file e).
# So white pawn at file d (4th file? no, 4 empty = files a,b,c empty, then P at d=file 3), black pawn at file e (file 4).
# Hmm, this FEN doesn't set up en passant correctly because black pawn just double-pushed from d7 to d5.
# The ep square would be d6 (row 2, file 3).
e.start()
# Manually construct en passant position
e.empty()
# black pawns row 1 (rank 7), white pawns row 6 (rank 2)
# Wait, I need black pawn at d5 (rank 5 = row 3) and white pawn at e5 (rank 5 = row 3).
# Let me just build it manually
for f in range(8):
    e.B[sq(f, 0)] = 32 | 1  # black back rank (row 0)
    e.B[sq(f, 7)] = 32  # white back rank (row 7)
for f in range(8):
    e.B[sq(f, 6)] = 8  # white pawns row 6
    e.B[sq(f, 1)] = 9  # black pawns row 1
# Now set up en passant: black pawn double-pushed from d7 (row 1) to d5 (row 3)
# white pawn e5 (row 3, file 4) can capture
e.B[sq(3, 3)] = 9  # black pawn d5
e.B[sq(4, 3)] = 8  # white pawn e5
e.ep = sq(3, 2)  # ep square d6
e.kings = [sq(4, 7), sq(4, 0)]  # white king e1, black king e8
# Now white (side 0) should generate exd6 ep capture
moves = e.gen(0)
print('Test3: white moves with ep')
for m in moves:
    uf = e.fa(m); ut = e.ta(m)
    uf_chess = uf % 8  # file
    uf_r = uf // 8
    ut_chess = ut % 8
    ut_r = ut // 8
    print(' ', 'abcdefgh'[uf % 8] + str(8 - uf_r) if False else 'a6', 'to', 'a4', 'priv', e.pr_(m))

# Actually let me just print all moves
for m in moves:
    print(' ', e.sq2uci(m) if hasattr(e, 'sq2uci') else 'x')
print('done')
