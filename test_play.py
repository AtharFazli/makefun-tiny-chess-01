import importlib.util, sys
spec = importlib.util.spec_from_file_location("ec", "/home/fazly/makefun/work/tiny-chess/src.py")
ec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)
ec.start()
# generate pseudo-legal moves for white
L = ec.gen(0)
print("pseudo-legal moves:", len(L))
# check a few moves are legal
import random
random.seed(1)
for _ in range(3):
 m = random.choice(L)
 ok = ec.is_legal(0, m)
 print("move", ec.uc(m), "legal:", ok)
