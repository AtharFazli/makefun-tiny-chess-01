import lzma
data=open('/home/fazly/makefun/work/tiny-chess/main.py','rb').read()
print('size',len(data))
print('first6',data[:6])
try:
    d=lzma.decompress(data)
    print('lzma decompress OK:',len(d),'bytes')
    print(d[:200])
except Exception as e:
    print('lzma error:',e)
