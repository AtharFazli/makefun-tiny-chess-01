import hashlib,os
p='/home/fazly/makefun/work/tiny-chess/src.py'
print('src.py size', os.path.getsize(p))
print('src.py sha256', hashlib.sha256(open(p,'rb').read()).hexdigest())
main='/home/fazly/makefun/work/tiny-chess/main.py'
data=open(main,'rb').read()
print('main.py size', len(data))
print('main.py sha256', hashlib.sha256(data).hexdigest())
# find import lines in main
idx=data.find(b'import')
print('main.py first import bytes', data[idx:idx+40])
