import importlib.util
spec = importlib.util.spec_from_file_location("ec", "/home/fazly/makefun/work/tiny-chess/src.py")
ec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)
ec.start()
# At start, white to move. search(0,...) is white's score, search(1,...) is black's score (neg of white).
print("search(0,2):", ec.search(0,2,-100000,100000))
print("search(1,2):", ec.search(1,2,-100000,100000))
print("neg search(1,2) == search(0,2)?", ec.search(0,2,-100000,100000)==-ec.search(1,2,-100000,100000))
# now flip: make white move d2d4, then it's black to move. search(1,...) should be black's score.
ec.make(ec.parse_uci('e2e4'))
print("after e2e4, side to move: black. search(1,1):", ec.search(1,1,-100000,100000))
print("white's score (neg):", -ec.search(1,1,-100000,100000))
ec.unmake(ec.parse_uci('e2e4'))
