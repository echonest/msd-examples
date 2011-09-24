
import simplejson as json
import sys


lines = []
which = 0

if len(sys.argv) > 1:
    which = int(sys.argv[1])

for line in sys.stdin:
    fields = line.strip().split('\t')
    if len(fields) == 2:
        key, sval = fields
        if len(sval) > 0:
            list = json.loads(sval)
            lines.append( (key, list))

lines.sort(reverse=True, key=lambda s:s[1][which])


for key, val in lines:
    print val, key
