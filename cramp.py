
"""
    A map-reduce that calculates the difference in 
    average volume between the first and the second
    half of the song.
"""

from mrjob.job import MRJob
import track
from itertools import imap
import unicodedata

# if YIELD_ALL is true, we yield all densities, otherwise,
# we yield just the extremes

YIELD_ALL = False

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
            first_count = 0
            second_count = 0

            xdata = []
            ydata = []
            for i in xrange(len(segments)):
                seg = segments[i]

                # bail out if we have a really long quiet segment
                # these are usually surprise hidden tracks

                if seg['loudness_max'] < -40 and seg['duration'] > 30:
                    return

                seg_loudness = seg['loudness_max'] * seg['duration']

                if seg['start'] + seg['duration'] <= half_track:
                    seg_loudness = seg['loudness_max'] * seg['duration']
                    first_half += seg_loudness
                    first_count += 1
                elif seg['start'] < half_track and seg['start'] + seg['duration'] > half_track:
                    # this is the nasty segment that spans the song midpoint.
                    # apportion the loudness appropriately
                    first_seg_loudness = seg['loudness_max'] * (half_track - seg['start'])
                    first_half += first_seg_loudness
                    first_count += 1

                    second_seg_loudness = seg['loudness_max'] * (seg['duration'] - (half_track - seg['start']))
                    second_half += second_seg_loudness
                    second_count += 1
                else:
                    seg_loudness = seg['loudness_max'] * seg['duration']
                    second_half += seg_loudness
                    second_count += 1

                xdata.append( seg['start'] )
                ydata.append( seg['loudness_max'] )

            # only yield data if we've had sufficient segments in the first
            # and second half of the track. (This is to avoid the proverbial
            # hidden tracks that have extreme amounts of leading or tailing
            # silene

            correlation = pearsonr(xdata, ydata)
            if first_count > 10 and second_count > 10:
                ramp_factor = second_half / half_track - first_half / half_track
                #if YIELD_ALL or ramp_factor > 10 or ramp_factor < -10:
                if YIELD_ALL or ramp_factor > 10 and correlation > .5:
                    yield (t['artist_name'], t['title'], t['track_id'], correlation), ramp_factor

    # no need for a reducer
    #def reducer(self, key, val):
        #yield (key, sum(val))


def pearsonr(x, y):
  # Assume len(x) == len(y)
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x_sq = sum(map(lambda x: pow(x, 2), x))
    sum_y_sq = sum(map(lambda x: pow(x, 2), y))
    psum = sum(imap(lambda x, y: x * y, x, y))
    num = psum - (sum_x * sum_y/n)
    den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)
    if den == 0: 
        return 0
    return num / den


def test():
    x = [1,2,3,4,5,6,7,8,9,10]
    y = [10, 20, 35, 45, 47, 60, 70, 87, 91, 100]
    print pearsonr(x,y)


if __name__ == '__main__':
    MRRamp.run()
