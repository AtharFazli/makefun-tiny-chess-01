import lzma

p='/home/fazly/makefun/work/tiny-chess/main.py'
data=open(p,'rb').read()
head=b"#coding:l1\nimport lzma;exec(lzma.decompress('"
tail=b"'.encode('l1'))\n"
i=data.find(head)
j=data.find(tail,i)
payload=data[i+len(head):j]
# decode literal byte by byte (mimicking compressLiteral inverse)
out=[]
k=0
n=len(payload)
while k<n:
    b=payload[k]
    if b!=92:  # backslash
        out.append(b); k+=1; continue
    # backslash
    if k+1>=n:
        print('trailing backslash at', k); break
    c=payload[k+1]
    if c==110: out.append(10)          # \n
    elif c==114: out.append(13)        # \r
    elif c==92: out.append(92)         # \\
    elif c==39: out.append(39)         # \'
    elif c==120:  # \xNN
        if k+3>=n:
            print('bad \\x at', k); break
        hx=payload[k+2:k+4]
        try:
            out.append(int(hx,16))
        except:
            out.append(hx[0]); 
            print('bad hex', hx); break
        k+=3
    else:
        out.append(c)
    k+=2
print('decoded len', len(out))
try:
    payload2=lzma.decompress(bytes(out))
    print('lzma decompress OK, len', len(payload2))
    print('has import json:', b'import json' in payload2)
    src=open('/home/fazly/makefun/work/tiny-chess/src.py','rb').read()
    print('matches src.py:', payload2==src)
except Exception as e:
    print('lzma err:', e)
