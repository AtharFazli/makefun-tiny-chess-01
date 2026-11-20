import sys
sys.path.insert(0,'/home/fazly/makefun/work/tiny-chess')
import src
src.start()
B0=list(src.B)
def legal_moves(side):
    L=[]
    for m in src.gen(side):
        src.make(m)
        if not src.katt(side):
            L.append(m)
        src.unmake(m)
    return L
def greedy(movs):return movs[0]
def play(move_fn, side, maxply=200):
    src.start()
    for i in range(maxply):
        movs=[m for m in src.gen(side) if not src.katt(side)]
        if not movs:
            return ('no legal move',side,i)
        m=move_fn(movs)
        src.make(m)
        side=opp(side)
        src.unmake(m)
    return ('max plies',maxply)
w=legal_moves(0)
print('legal white:',len(w))
b=legal_moves(1)
print('legal black:',len(b))
m=w[0]
src.make(m);src.unmake(m)
print('board restored after round trip:',src.B==B0)
res=play(greedy,0)
print('game:',res)
print('board restored after game:',src.B==B0)
