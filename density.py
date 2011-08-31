"""
    A map-reduce that calculates the density for each
    of a set of tracks.  The track density is the average
    number of segments per segment for a track.
"""

from mrjob.job import MRJob
import track

# if YIELD_ALL is true, we yield all densities, otherwise,
# we yield just the extremes

YIELD_ALL = True

class MRDensity(MRJob):
    """ A  map-reduce job that calculates the density """

    def mapper(self, _, line):
        """ The mapper loads a track and yields its density """
        t = track.load_track(line)
        if t:
            if t['tempo'] > 0:
                density = len(t['segments']) / t['duration']
                #only output extreme density
                if YIELD_ALL or density > 8 or density < .5:
                    yield (t['artist_name'], t['title'], t['song_id']), density

    # no need for a reducer
    #def reducer(self, key, val):
        #yield (key, sum(val))

if __name__ == '__main__':
    MRDensity.run()
