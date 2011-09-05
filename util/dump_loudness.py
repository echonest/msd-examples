import sys
from pyechonest import track

WEIGHT = 10
def dump_loudness(id):
    t = track.track_from_id(id)
    print "# ID ", id
    print "#", t.title, 'by', t.artist
    print "#"
    weighted = []
    half_track = t.duration / 2
    first_half = 0
    second_half = 0

    for seg in t.segments:
        loudness = seg['loudness_max']
        weighted.append(loudness)
        if len(weighted) > WEIGHT:
            weighted.pop(0)
        avg = sum(weighted) / len(weighted)

        seg_loudness = seg['loudness_max'] * seg['duration']

        if seg['start'] < half_track:
            first_half += seg_loudness
        else:
            second_half += seg_loudness

        ramp_factor = second_half / half_track - first_half / half_track
        #print seg['start'], loudness, avg, first_half, second_half, ramp_factor
        print "%8.6f %9.4f %9.4f %12.6f %12.6f %12.6f" % (seg['start'], loudness, avg, first_half, second_half, ramp_factor)

    print "#"
    print "#", 'ramp factor', ramp_factor

if __name__ == '__main__':
    dump_loudness(sys.argv[1])
