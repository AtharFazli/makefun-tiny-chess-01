import importlib.util
spec = importlib.util.spec_from_file_location("ec", "/home/fazly/makefun/work/tiny-chess/src.py")
ec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)
# white: Q+rook vs black king (clear material win)
fen = '4k3/8/8/8/8/8/8/4RK3 w - - 0 1'
ec.setup(fen)
legal = ec.gen(0)
print("legal:", len(legal), ec.uc(legal[0]) if legal else None)
best = ec.choose(fen, [ec.uc(m) for m in legal])
print("white Q+rook vs K:", best)
# black to move, black is in check? no. black K vs white Q+R -> black loses.
fen2 = '4k3/8/8/8/8/8/8/4RK3 b - - 0 1'
ec2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(ec2)
ec2.setup(fen2)
legal2 = ec2.gen(1)
best2 = ec2.choose(fen2, [ec2.uc(m) for m in legal2])
print("black loses:", best2)
