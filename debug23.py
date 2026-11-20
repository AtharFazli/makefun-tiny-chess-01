p='/home/fazly/makefun/work/tiny-chess/main.py'
data=open(p,'rb').read()
head=b"#coding:l1\nimport lzma;exec(lzma.decompress('"
tail=b"'.encode('l1'))\n"
i=data.find(head)
j=data.find(tail,i)
raw=data[i+len(head):j]
print('raw literal length', len(raw))
print('raw literal first 40 bytes:', raw[:40])
# count NUL bytes in raw
print('NUL count in raw:', raw.count(b'\x00'))
# decode raw as latin1 and count backslash escapes
s=raw.decode('latin-1')
print('has backslash:', '\\\\' in s)
print('backslash count:', s.count('\\'))
# show first 60 chars of the literal string
print('literal first 60 chars:', repr(s[:60]))
