import lzma

src = open('/home/fazly/makefun/work/tiny-chess/src.py','rb').read()
# Pack src.py with raw lzma (the way the kit's stub decompresses)
payload = lzma.compress(src, format=lzma.FORMAT_RAW)
body = payload.decode('latin-1')
stub = "#coding:l1\nimport lzma;exec(lzma.decompress('"
stub += body
stub += "'.encode('l1'))\n"
open('/home/fazly/makefun/work/tiny-chess/main_pytest.py','wb').write(stub.encode('latin-1'))
print('written main_pytest.py', len(stub))
# verify decompress
h=b"#coding:l1\nimport lzma;exec(lzma.decompress('"
t=b"'.encode('l1'))\n"
i=stub.find(h); j=stub.find(t,i)
raw=stub[i+len(h):j].encode('latin-1')
dec=lzma.decompress(raw)
print('decoded len', len(dec), 'matches src:', dec==src)
print('has import json:', b'import json' in dec)
