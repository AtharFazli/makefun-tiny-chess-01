import importlib.util
spec = importlib.util.spec_from_file_location("ec", "/home/fazly/makefun/work/tiny-chess/src.py")
ec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)
ec.start()
L = ec.gen(0)
legal = [ec.uc(m) for m in L if ec.is_legal(0, ec.parse_uci(ec.uc(m)))]
print("legal moves:", len(legal))
best = ec.choose('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', legal)
print("best move:", best)
