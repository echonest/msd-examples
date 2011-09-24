

"""
    A map-reduce that calculates the difference in 
    average volume between the first and the second
    half of the song.
"""

from mrjob.job import MRJob
import track
from itertools import imap
import math
import tools
import sys

# if YIELD_ALL is true, we yield all densities, otherwise,
# we yield just the extremes

YIELD_ALL = False

class MRlmatch(MRJob):
    """ A  map-reduce job that calculates the ramp factor """

    DUMP = False
    SIZE = 64
    VECTOR = True
    #MATCH = tools.rnormalize(tools.scale(tools.sin2wave(SIZE), 60, -60), -60, 0)
    MATCH = tools.rnormalize(tools.scale(tools.sinwave(SIZE), 60, -60), -60, 0)

    def mapper(self, _, line):
        """ The mapper loads a track and yields its ramp factor """
        t = track.load_track(line)
        segments = t['segments']
        duration = t['duration']
        xdata = []
        ydata = []
        for i in xrange(len(segments)):
            seg = segments[i]
            sloudness = seg['loudness_max']
            sstart = seg['start'] + seg['loudness_max_time']
            xdata.append( sstart )
            ydata.append( sloudness )

        if duration > 20:
            idata = tools.interpolate(xdata, ydata, int(duration) * 10)
            smooth = tools.smooth(idata, 20)
            samp = tools.sample(smooth, self.SIZE)
            ndata = tools.rnormalize(samp, -60, 0)
            if self.DUMP:
                for i, (x, y) in enumerate(zip(self.MATCH, ndata)):
                    print i, x, y
            if self.VECTOR:
                yield (t['artist_name'], t['title'], t['track_id']), ndata
            else:
                distance = tools.distance(self.MATCH, ndata)
                yield (t['artist_name'], t['title'], t['track_id']), distance


    # no need for a reducer
    #def reducer(self, key, val):
        #yield (key, sum(val))


def dump():
    data = tools.rnormalize(tools.scale(tools.sin2wave(256), 60, -60), -60, 0)
    for d in data:
        print d

if __name__ == '__main__':
    #dump()
    MRlmatch.run()
