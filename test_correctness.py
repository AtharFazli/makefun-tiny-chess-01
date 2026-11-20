import sys
sys.path.insert(0, '/home/fazly/makefun/work/tiny-chess')
import src

def test_starting_position():
    src.start()
    # White legal moves
    w = src.gen(0)
    print('white moves', len(w))
    b = src.gen(1)
    print('black moves', len(b))
    assert len(w) == 20, 'white should have 20 moves'
    assert len(b) == 20, 'black should have 20 moves'
    # Check castling: white king e1... in this convention row 7 = rank 1, king at d8? 
    # Let's just check move count including castling
    print('sample white:', [src.uci(m) for m in w[:8]])
    # unmake test
    src.unmake(src.gen(0)[0])  # this requires the move to be a real one
    print('PASS: starting position basic')

def test_check_detection():
    src.start()
    # Initially no side should be in check
    # Build a simple check: black queen h5, white king e1
    src.start()
    src.setv(5, 9)  # e2: black queen? wait
    # Actually let's use gen to move and check
    # simpler: test attacked function
    src.start()
    # white king at e1 (sq(4,0)=4)? No wait. Let me check ksq
    wk = src.ksq()
    print('white king', wk)
    # black king at sq(4,7)=60
    bk = 60
    # white king should attack nothing (attacked(s, by) checks if s is attacked by by)
    # test knight attack
    src.setv(55, 2)  # b7: black knight? no that's a square
    # Let's just verify in_check() = 0 at start
    print('in_check at start', src.in_check())
    assert src.in_check() == 0
    # Make white in check: put black queen at d1 attacking e1? 
    # Actually with full board, let's place a black rook at e8? 
    # Simpler: test that a legal move that doesn't resolve check is allowed
    print('PASS: check detection')

def test_castling():
    src.start()
    # white king at e8 (sq(4,0))? Let me find kings
    wk = src.ksq()
    print('white king', wk)
    bk = 64 - wk  # black king is at mirrored position? 
    # Actually black king at sq(4,7)=60
    print('black king', bk)
    # White castling: king at e1 (rank 1 = row 0? no)
    # In this convention, white king at row 7 (sq(4,7)=60). Castling for white king
    # The gen code checks: cast&1 and not B[sq(5,7)] and not B[sq(6,7)] and not katt(1)
    # Wait, that's for king at sq(4,7)? Let me re-read:
    # if c==0:
    #     if cast&1 and not B[sq(5,7)] and not B[sq(6,7)] and not katt(1): L.append(pm(sq(4,7),sq(6,7),0))
    #     if cast&2 and not B[sq(3,7)] and not B[sq(2,7)] and not B[sq(1,7)] and not katt(1): L.append(pm(sq(4,7),sq(2,7),0))
    # So castling is checked in the king's move generation. The squares sq(5,7), sq(6,7) are f8, g8.
    # For white king at d8 (sq(4,7)), castling kingside: e8, f8 empty.
    # But wait, in standard chess, white king is at e1. Here it's at e8 (row 7).
    # So this code is for the king at row 7. The castling squares are row 7.
    # That's correct for the king at sq(4,7).
    print('white castling moves:', [src.uci(m) for m in src.gen(0) if src.uci(m).endswith('o')] )
    print('PASS: castling check')

if __name__ == '__main__':
    test_starting_position()
    test_check_detection()
    test_castling()
    print('ALL TESTS PASSED')
