import sys,os

file_path = os.path.join(os.path.dirname(sys.argv[0]),"patch_maker_usage.txt")
f = open(file_path,'r')
lines = f.read()
print lines
