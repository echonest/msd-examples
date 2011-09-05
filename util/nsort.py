
import sys


lines = []
for line in sys.stdin:
    fields = line.strip().split('\t')
    if len(fields) == 2:
        key, sval = fields
        if len(sval) > 0:
            lines.append( (key, float(sval)) )

lines.sort(reverse=True, key=lambda s:s[1])


for key, val in lines:
    print val, key
