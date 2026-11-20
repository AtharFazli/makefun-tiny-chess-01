import importlib.util
spec = importlib.util.spec_from_file_location('ec', '/home/fazly/makefun/work/tiny-chess/src.py')
ec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)
ec.start()
print('N0 before:', ec.N0[0])
ec.search(0,2,-100000,100000)
print('N0 after:', ec.N0[0])
