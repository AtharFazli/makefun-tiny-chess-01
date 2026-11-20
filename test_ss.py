import importlib.util
spec = importlib.util.spec_from_file_location("ec", "/home/fazly/makefun/work/tiny-chess/src.py")
ec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)
# semi-slav opening: d2d4 d7d5 c2c4 c7c6 b1c3 g8f6 e2e3 e7e6
fen='rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1'
ec.setup(fen)
L = ec.gen(0)
legal = [ec.uc(m) for m in L if ec.is_legal(0, m)]
# pick first legal move (d2d4), apply it
m = legal[0]
mi = ec.parse_uci(m)
print("root legal:", len(legal), "first:", m)
ec.make(mi)
# after white plays d4, black plays d5, white c4, black c6, white b3, black f6, white e3, black e6
# The fen after 8 plies.
fen='rnbqkbnr/pp2pppp/8/3p4/3PP3/8/PPP2PP1/RNBQKBNR w KQkq - 0 1'
ec.setup(fen)
L2 = ec.gen(0)
legal2 = [ec.uc(m) for m in L2 if ec.is_legal(0, m)]
print("semi-slav legal:", len(legal2))
best = ec.choose(fen, legal2)
print("best:", best)
