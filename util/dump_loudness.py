import sys
import re
from itertools import imap
from pyechonest import track
import spotimeta

WEIGHT = 10

def dump_loudness(id, file=sys.stdout):
    t = track.track_from_id(id)
    title = t.title + ' by ' + t.artist
    spotify_id = get_spotify_id(t.artist, t.title)

    print >>file, "# ID ", id
    print >>file, "#", title
    print >>file, "# ARTIST ", t.artist
    print >>file, "# TITLE ", t.title
    print >>file, "# SONG_ID ", t.song_id
    print >>file, "# SPOT_ID ", spotify_id
    print >>file, "#"

    weighted = []
    half_track = t.duration / 2
    first_half = 0
    second_half = 0

    xdata = []
    ydata = []

    for seg in t.segments:
        sstart = seg['start']
        sloudness = min(seg['loudness_max'], 0)
        sloudness = max(sloudness, -60)
        sduration = seg['duration']
        send = sstart + sduration

        weighted.append(sloudness)
        if len(weighted) > WEIGHT:
            weighted.pop(0)
        avg = sum(weighted) / len(weighted)

        if send <= half_track:
            seg_loudness = sloudness * sduration
            first_half += seg_loudness
        elif sstart < half_track and send > half_track:
            # this is the nasty segment that spans the song midpoint.
            # apportion the loudness appropriately
            first_seg_loudness = sloudness * (half_track - sstart)
            first_half += first_seg_loudness

            second_seg_loudness = sloudness * (send - half_track)
            second_half += second_seg_loudness
        else:
            seg_loudness = sloudness * sduration
            second_half += seg_loudness

        xdata.append( sstart )
        ydata.append( sloudness )

        ramp_factor = second_half / half_track - first_half / half_track
        #print >>file, seg['start'], sloudness, avg, first_half, second_half, ramp_factor
        #print >>file, "%8.6f %9.4f %9.4f %12.6f %12.6f %12.6f" % (sstart, sloudness, avg, first_half, second_half, ramp_factor)
        print >>file, "%8.6f %9.4f %9.4f" % (sstart, sloudness, avg)

    correlation = pearsonr(xdata, ydata)
    print >>file, "#"
    print >>file, "#", 'ramp factor', ramp_factor
    print >>file, "#", 'correlation', correlation
    print >>file, "#", 'first', first_half / half_track
    print >>file, "#", 'second', second_half / half_track
    print >>file, "#"

    return title, ramp_factor, first_half / half_track, second_half / half_track

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


def spotify_search(name):
    retries = 5
    while retries > 0:
        try:
            results = spotimeta.search_track(name)
            return results
        except spotimeta.ServerError:
            print >> sys.stderr, "      ... retrying spotify for ", name
            time.sleep(5)
            retries -= 1
    return None
            
def get_spotify_id(artist, title):
    name = artist + ' ' + title
    name = norm(name)

    search = spotify_search(name)
    if search and search["total_results"] > 0:
        best = search['result'][0]
        result = best['href']
        print >> sys.stderr, '    found', result, best['artist']['name'], best['name']
        return result
    else:
        print >> sys.stderr, "Couldn't spotifind", name
        return None

def norm(name):
    s = name
    s = s.replace(".", "")
    s = s.lower()
    s = re.sub(r'&', ' and ', s)
    s = re.sub(r' +', ' ', s)
    s = s.strip()

    # if we've normalized away everything
    # keep it.
    if len(s) == 0:
        s = name
    return s



if __name__ == '__main__':
    dump_loudness(sys.argv[1])
