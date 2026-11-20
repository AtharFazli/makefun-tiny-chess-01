import lzma, hashlib

src = open('/home/fazly/makefun/work/tiny-chess/src.py','rb').read()
# mimic the kit: compress with lzma level 9, wrap in stub
payload = lzma.compress(src, format=lzma.FORMAT_RAW, filters=[lzma.FILTER_DELTA] if False else [{'id': lzma.ALGO_LZMA1, 'mode': lzma.MODE_NORMAL, 'dict_size': 2**25, 'lc': 3, 'lp': 0, 'pb': 0}])
stub = b"#coding:l1\nimport lzma;exec(lzma.decompress('"
# literal encode similar to kit
def literal_encode(payload_bytes):
    out = bytearray()
    for b in payload_bytes:
        if b == 0:
            out += b"\\x00"
        elif b == 13: out += b"\\r"
        elif b == 10: out += b"\\n"
        elif b == 92: out += b"\\\\"
        elif b == 39: out += b"\\'"
        else: out.append(b)
    return bytes(out)
# actually use the kit's literal (for correctness, just test raw lzma wrapper)
body = literal_encode(payload)
stub2 = stub + body + b"'.encode('l1'))\n"
open('/home/fazly/makefun/work/tiny-chess/main_pytest.py','wb').write(stub2)
print('test main.py written', len(stub2))

# now decompress and check
head=b"#coding:l1\nimport lzma;exec(lzma.decompress('"
tail=b"'.encode('l1'))\n"
i=stub2.find(head); j=stub2.find(tail,i)
pl=stub2[i+len(head):j]
# decompress raw lzma
try:
    dec = lzma.decompress(pl, format=lzma.FORMAT_RAW, filters=[{'id': lzma.ALGORITHM_LZMA1, 'mode': lzma.MODE_NORMAL}])
    print('decompressed len', len(dec))
    print('matches src.py:', dec == src)
    print('has import json:', b'import json' in dec)
    print('has import urllib:', b'import urllib' in dec)
    print('has import sys:', b'import sys' in dec)
    print('has import lzma:', b'import lzma' in dec)
except Exception as e:
    print('err', e)
    print('first 40 dec bytes', dec[:40] if 'dec' in dir() else 'n/a')
