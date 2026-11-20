import lzma

p='/home/fazly/makefun/work/tiny-chess/main.py'
data=open(p,'rb').read()
head=b"#coding:l1\nimport lzma;exec(lzma.decompress('"
tail=b"'.encode('l1'))\n"
i=data.find(head)
j=data.find(tail,i)
payload=data[i+len(head):j]
s=payload.decode('latin-1')
out=[]
k=0
n=len(s)
while k<n:
    c=s[k]
    if c!='\\\\':
        out.append(c); k+=1; continue
    if k+1>=n: print('trailing backslash'); break
    nxt=s[k+1]
    if nxt=='n': out.append('\n'); k+=2
    elif nxt=='r': out.append('\r'); k+=2
    elif nxt=='\\': out.append('\\'); k+=2
    elif nxt=="'": out.append("'"); k+=2
    elif nxt=='x':
        if k+4>n: print('bad \\x'); break
        out.append(chr(int(s[k+2:k+4],16))); k+=4
    elif nxt=='0':
        out.append('\x00'); k+=2
    else:
        out.append(nxt); k+=2
raw=''.join(out).encode('latin-1')
print('literal bytes len', len(raw))
print('first 16 raw bytes', raw[:16].hex(' '))
print('has lzma magic 5d00:', raw[:2]==b'\x5d\x00')
# try different lzma decoders
for fmt in [lzma.FORMAT_AUTO, lzma.FORMAT_RAW]:
    try:
        dec=lzma.decompress(raw, format=fmt)
        print('fmt', fmt, 'OK len', len(dec))
        print('has import json:', b'import json' in dec)
        src=open('/home/fazly/makefun/work/tiny-chess/src.py','rb').read()
        print('matches src:', dec==src)
        break
    except Exception as e:
        print('fmt', fmt, 'err:', e)
