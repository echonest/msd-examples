import time
import json
import re
import sys
import os


def get_plot_info(id):
    path = id + ".out"
    tid = ''
    sid = ''
    spot = None
    name = ''
    factor = 0
    first = 0
    second = 0
    correlation = 0

    if os.path.exists(path):
        f = open(path)
        for which, line in enumerate(f):
            if which == 1:
                name = line.strip().replace("# ", "")
            elif line[0] == '#':
                fields = line.strip().split()
                if len(fields) >= 4 and fields[1] == 'ramp':
                    factor = float(fields[3])
                if len(fields) >= 3 and fields[1] == 'first':
                    first = float(fields[2])
                if len(fields) >= 3 and fields[1] == 'second':
                    second = float(fields[2])
                if len(fields) >= 3 and fields[1] == 'correlation':
                    correlation = float(fields[2])
                if len(fields) >= 3 and fields[1] == 'ID':
                    tid = fields[2]
                if len(fields) >= 3 and fields[1] == 'SONG_ID':
                    sid = fields[2]
                if len(fields) >= 3 and fields[1] == 'SPOT_ID' and fields[2] <> 'None':
                    spot = fields[2]

        if tid <> id:
            print >> sys.stderr, "Mismatched ID ", id, tid
        return name, sid, spot, factor, first, second, correlation
    else:
        return None


def make_entry(id):
    info = get_plot_info(id)
    if info:
        name, sid, spot_id, factor, first, second, correlation = info
        image = id + ".png"

        title = name

        if spot_id:
            print '<a href=\"' + spot_id + '">',
            print '<img src="plots/' + image + '">',
            print '</a>'
        else:
            pass
            # print '<img src="plots/' + image + '">'
    else:
        print >>sys.stderr, "Can't open info for", id
    
def make_plot_page(index):
    for l in index:
        process_plot(l.strip());


def header():
    print "<html>"
    print "<head>"
    print "<title>"
    print "Loudness curves from the Million Song Dataset"
    print "</title>"
    print "</head>"
    print "<body>"
    print "<h1> Loudness curves from the Million Song Dataset </h1>"

def footer():
    print "<hr>"
    print "</body>"

def build_page(index):
    header()
    for count, l in enumerate(open(index)):
        l = l.strip()
        print >> sys.stderr, count, l
        if len(l) > 0:
            if l[0] == '#':
                print "<h2>", l[1:], "</h2>"
            elif l.startswith("TR"):
                make_entry(l)
    footer()


def qd_page():
    header()
    for l in sys.stdin:
        plot = l.strip()
        print '<img src="' + plot + '">',
    footer()

def dump_ids():
    # parses input in the form
    # # 30.8926305957 ["David Coverdale", "Into The Light", "TRPNADQ128F422DB22"]
    for which, line in  enumerate(sys.stdin):
        fields = line.strip().split()
        slist = ' '.join(fields[1:])
        list = json.loads(slist)
        id = list[2]
        print id


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--dump':
            dump_ids()
        else:
            build_page(sys.argv[1])
    else:
        qd_page()

