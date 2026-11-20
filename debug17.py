with open('/home/fazly/makefun/work/tiny-chess/src.py') as f:
    lines=f.readlines()
print('line1 repr:', repr(lines[0]))
print('has json:', 'json' in lines[0])
