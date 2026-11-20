import importlib.util
spec = importlib.util.spec_from_file_location("ec", "/home/fazly/makefun/work/tiny-chess/src.py")
ec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)
ec.start()
# after white e2e4, it's black to move
fen = 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1'
L = ec.gen(1)
legal = [ec.uc(m) for m in L if ec.is_legal(1, ec.parse_uci(ec.uc(m)))]
print("black legal:", len(legal), legal[:5])
best = ec.choose(fen, legal)
print("choose (black) best:", best)
