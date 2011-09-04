
import sys


lines = []
for line in sys.stdin:
    key, sval = line.split('\t')
    lines.append( (key, float(sval)) )
    lines.sort(reverse=True, key=lambda s:s[1])


for key, val in lines:
    print val, key
