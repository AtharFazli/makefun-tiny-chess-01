import sys
sys.path.insert(0,'/home/fazly/makefun/work/tiny-chess')
import src
src.start()
B0=list(src.B)
# pick a white pawn move
m=src.gen(0)[0]
print('move',src.uci(m),'m',m)
src.make(m)
d1=list(src.B)
src.unmake(m)
d2=list(src.B)
print('after make+unmake equal:',d1==d2)
print('board equal after roundtrip:',d2==B0)
# find diffs
for i in range(64):
    if B0[i]!=d2[i]:
        print('diff at',i,'orig',B0[i],'after',d2[i])
# check ep, cast
print('ep before',src.ep,'after',src.ep)
print('cast before',src.cast,'after',src.cast)
# castling rights after king e1 (no rook moves) should be unchanged
