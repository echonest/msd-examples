# 30.8926305957 ["David Coverdale", "Into The Light", "TRPNADQ128F422DB22"]

import simplejson as json
import sys
import os
import sdir
import dump_loudness

plotter_text = """
set terminal postscript landscape size 8.4,5.9
set output "foo.plt"
set style data line
set key bottom
set xlabel "seconds"
set ylabel "decibels"
set title " %s "
plot "%s.out" using 1:2 with line linecolor rgb "#aaffaa" title "raw loudness"
replot "%s.out" using 1:2 with line lt -1 linecolor rgb "blue" smooth bezier title "smoothed loudness"
replot %f with line linecolor rgb "#777777" title ""
replot %f with line linecolor rgb "#777777" title ""
set key title "score:%.2f ramp:%.2f corr:%.2f"
set terminal postscript landscape size 8.4,5.9
set output "plot.ps"
replot
"""

def make_plot(id, force=False):
    plot_path = os.path.join("plots", id + ".png")
    if force or not os.path.exists(plot_path):
        print "Creating plot", plot_path
        name, ramp, first, second, correlation = sdir.get_plot_info(id)
        score = ramp * correlation
        title = name.replace('"', "'")
        plotter = open("plotter.gplt", "w")
        print >>plotter, plotter_text % (title, id, id, first, second, score, ramp, correlation)
        plotter.close()
        os.system("gnuplot plotter.gplt")
        os.system("convert -rotate 90 plot.ps %s" % (plot_path,))
    else:
        print >>sys.stderr, "   plot exists, skipping...", plot_path

def create_plot(id):
    force = False
    path = id + ".out"
    if not os.path.exists(path):
        f = open(path, "w")
        dump_loudness.dump_loudness(id, f)
        f.close()
        force = True
    else:
        print >>sys.stderr, "   data exists, skipping...", id
    make_plot(id, force)


def create_plots():
    # parses input in the form
    # # 30.8926305957 ["David Coverdale", "Into The Light", "TRPNADQ128F422DB22"]
    for which, line in  enumerate(sys.stdin):
        fields = line.strip().split()
        slist = ' '.join(fields[1:])
        list = json.loads(slist)
        id = list[2]
        print >>sys.stderr, which, id
        create_plot(id)



if __name__ == '__main__':
    if len(sys.argv) > 1:
        for id in sys.argv[1:]:
            create_plot(id)
    else:
        create_plots()
    
