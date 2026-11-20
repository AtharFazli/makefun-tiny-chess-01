import lzma,subprocess,sys
p='/home/fazly/makefun/work/tiny-chess/main.py'
data=open(p,'rb').read()
# the payload is between HEAD and TAIL
head=b"#coding:l1\nimport lzma;exec(lzma.decompress('"
tail=b"'.encode('l1'))\n"
i=data.find(head)
j=data.find(tail,i)
print('head found', i, 'tail after', j)
payload=data[i+len(head):j]
print('payload length', len(payload))
# decompress
try:
    dec=lzma.decompress(payload)
    print('decompressed', len(dec), 'text head:', dec[:120])
    print('has import json:', b'import json' in dec)
    print('has import lzma:', b'import lzma' in dec)
except Exception as e:
    print('decompress err', e)
# compare with src.py
src=open('/home/fazly/makefun/work/tiny-chess/src.py','rb').read()
print('src.py has import json:', b'import json' in src)
print('src.py sha256', __import__('hashlib').sha256(src).hexdigest())
