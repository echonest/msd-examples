import sys
from pyechonest import track

def dump_loudness(id):
    t = track.track_from_id(id)
    for seg in t.segments:
        print seg['start'], seg['loudness_max']

if __name__ == '__main__':
    dump_loudness(sys.argv[1])
