with open('/home/fazly/makefun/work/tiny-chess/src.py') as f:
    lines = f.readlines()
for i in range(34, 48):
    print(i+1, repr(lines[i]))
