import lzma

p='/home/fazly/makefun/work/tiny-chess/main.py'
data=open(p,'rb').read()
head=b"#coding:l1\nimport lzma;exec(lzma.decompress('"
tail=b"'.encode('l1'))\n"
i=data.find(head)
j=data.find(tail,i)
payload=data[i+len(head):j]
# decode literal: treat payload as Latin-1 chars, then parse escapes
s=payload.decode('latin-1')
out=[]
k=0
n=len(s)
while k<n:
    c=s[k]
    if c!='\\\\':
        out.append(c); k+=1; continue
    # backslash
    if k+1>=n:
        print('trailing backslash'); break
    nxt=s[k+1]
    if nxt=='n': out.append('\n'); k+=2
    elif nxt=='r': out.append('\r'); k+=2
    elif nxt=='\\': out.append('\\'); k+=2
    elif nxt=="'": out.append("'"); k+=2
    elif nxt=='x':  # \xNN
        if k+4>n:
            print('bad \\x'); break
        hx=s[k+2:k+4]
        out.append(chr(int(hx,16))); k+=4
    elif nxt=='0':  # \0 or \x00
        # followed by optional hex digit (the kit writes \x0 then digit? no)
        out.append('\x00'); k+=2
    else:
        out.append(nxt); k+=2
print('decoded len', len(out))
try:
    payload2=lzma.decompress(''.join(out).encode('latin-1'))
    print('lzma decompress OK len', len(payload2))
    print('has import json:', b'import json' in payload2)
    src=open('/home/fazly/makefun/work/tiny-chess/src.py','rb').read()
    print('matches src.py:', payload2==src)
except Exception as e:
    print('lzma err:', e)
