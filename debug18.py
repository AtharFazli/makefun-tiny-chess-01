import lzma, re

p='/home/fazly/makefun/work/tiny-chess/main.py'
data=open(p,'rb').read()
head=b"#coding:l1\nimport lzma;exec(lzma.decompress('"
tail=b"'.encode('l1'))\n"
i=data.find(head)
j=data.find(tail,i)
payload=data[i+len(head):j]
# decode literal
out=[]
k=0
while k < len(payload):
    b=payload[k]
    if b==92: # backslash
        nxt=payload[k+1]
        if nxt==110: out.append(10)      # \n
        elif nxt==114: out.append(13)     # \r
        elif nxt==34: out.append(34)      # \"
        elif nxt==39: out.append(39)      # \'
        elif nxt==92: out.append(92)      # \\
        elif nxt==120:  # \xNN
            hexp=payload[k+2:k+4]; out.append(int(hexp,16)); k+=3
        elif nxt>=48 and nxt<=57:  # \00, \01, ... (NUL)
            # if next byte is digit, it's \00 form, else \N form (already handled)
            out.append(0); k+=1
        else:
            out.append(nxt)
        k+=1
    else:
        out.append(b); k+=1
dec=bytes(out)
try:
    payload2=lzma.decompress(dec)
    print('decompressed', len(payload2))
    print('has import json:', b'import json' in payload2)
    print('has import lzma:', b'import lzma' in payload2)
    print('has urllib:', b'urllib' in payload2)
    print('has import sys:', b'import sys' in payload2)
    # compare with src.py
    src=open('/home/fazly/makefun/work/tiny-chess/src.py','rb').read()
    print('matches src.py:', payload2==src)
except Exception as e:
    print('decompress err', e)
    print('dec first 50 bytes', dec[:50])
