import importlib.util
spec = importlib.util.spec_from_file_location("ec", "/home/fazly/makefun/work/tiny-chess/src.py")
ec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)
# Semi-slav: white to move, after 8 plies (d4,d5,c4,c6,b3,g6,e3,e6)
fen = 'rnbqkbnr/pp2pppp/8/3p4/3PP3/8/PPP2PP1/RNBQKBNR w KQkq - 0 1'
ec.setup(fen)
L = ec.gen(0)
legal = [ec.uc(m) for m in L if ec.is_legal(0, ec.parse_uci(ec.uc(m)))]
print("semi-slav white legal:", len(legal))
best = ec.choose(fen, legal)
print("choose (white):", best)
# Also test black-to-move version (engine plays black): after 9 plies (white played a9th? no)
# For black: the house made an extra move. Let's test a black-to-move position:
fen2 = 'rnbqkbnr/pp2pppp/8/3p4/3PP3/8/PPP2PP1/RNBQKBNR b KQkq - 0 1'
ec2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(ec2)
ec2.setup(fen2)
L2 = ec2.gen(1)
legal2 = [ec2.uc(m) for m in L2 if ec2.is_legal(1, ec2.parse_uci(ec2.uc(m)))]
print("semi-slav black legal:", len(legal2))
best2 = ec2.choose(fen2, legal2)
print("choose (black):", best2)
