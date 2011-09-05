
"""
    A map-reduce that calculates the difference in 
    average volume between the first and the second
    half of the song.
"""

from mrjob.job import MRJob
import track

# if YIELD_ALL is true, we yield all densities, otherwise,
# we yield just the extremes

YIELD_ALL = True

class MRRamp(MRJob):
    """ A  map-reduce job that calculates the ramp factor """

    def mapper(self, _, line):
        """ The mapper loads a track and yields its ramp factor """
        t = track.load_track(line)
        if t and t['duration'] > 60 and len(t['segments']) > 20:
            segments = t['segments']
            half_track = t['duration'] / 2
            first_half = 0
            second_half = 0

            for i in xrange(len(segments)):
                seg = segments[i]
                seg_loudness = seg['loudness_max'] * seg['duration']
                if seg['start'] < half_track:
                    first_half += seg_loudness
                else:
                    second_half += seg_loudness

            ramp_factor = second_half / half_track - first_half / half_track


            #only output extreme density
            if YIELD_ALL or density > 8 or density < .5:
                yield (t['artist_name'], t['title'], t['track_id']), ramp_factor

    # no need for a reducer
    #def reducer(self, key, val):
        #yield (key, sum(val))

if __name__ == '__main__':
    MRRamp.run()
