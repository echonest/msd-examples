
""" Processes track data from the Million Song Database.  Specifically, this
    file contains functions that load the flat-file format of tracks for the
    MSD. The format is one track per line, where each line is represented by 54
    fields as described here:  
    
    http://labrosa.ee.columbia.edu/millionsong/pages/field-list

    except that in the flat file format, the 'track id' field has been moved
    from field 52 to the first field.

    A track is represented as a dictionary.
"""

import sys
import pprint

def load_track(line):
    """ Loads a track from a single line """
    t = {}

    f = line.split('\t')
    if len(f) == 54:
        t['track_id'] = f[0]
        t['analysis_sample_rate'] = f[1]
        t['artist_7digitalid'] = f[2]
        t['artist_familiarity'] = float(f[3])
        t['artist_hotttnesss'] = float(f[4])
        t['artist_id'] = f[5]
        t['artist_latitude'] = float(f[6])
        t['artist_location'] = f[7]
        t['artist_longitude'] = float(f[8])
        t['artist_mbid'] = f[9]

        tag_words = f[10].split(',')
        tag_count = f[11].split(',')
        mbtags = [  (w, int(c))  for w,c in zip(tag_words, tag_count) if len(w) > 0]
        t['artist_mbtags'] = mbtags

        t['artist_name'] = f[12]
        t['artist_playmeid'] = int(f[13])

        artist_terms = f[14].split(',')
        artist_terms_freq = f[15].split(',')
        artist_terms_weight = f[16].split(',')
        t['artist_terms'] = [  (term, float(freq), float(weight)) \
            for term ,freq, weight in zip(artist_terms, artist_terms_freq, artist_terms_weight) if len(term) > 0]

        t['audio_md5'] = f[17]

        bars_confidence = f[18].split(',')
        bars_start = f[19].split(',')
        t['bars'] = [ (float(start), float(conf)) \
            for start, conf in zip(bars_start, bars_confidence) if len(start) > 0 ]

        beats_confidence = f[20].split(',')
        beats_start = f[21].split(',')
        t['beats'] = [ (float(start), float(conf)) \
            for start, conf in zip(beats_start, beats_confidence) if len(start) > 0 ]

        t['danceability'] = float(f[22])
        t['duration'] = float(f[23])
        t['end_of_fade_in'] = float(f[24])
        t['energy'] = float(f[25])
        t['key'] = (int(f[26]), float(f[27]))
        t['loudness'] = float(f[28])
        t['mode'] = (int(f[29]), float(f[30]))
        t['release'] = f[31]
        t['release_7digitalid'] = f[32]
        srid = f[32].zfill(10)
        t['cover_art'] = 'http://cdn.7static.com/static/img/sleeveart/%s/%s/%s/%s_200.jpg' \
            % (srid[0:2], srid[2:5], srid[5:8],  srid)

        sections_confidence = f[33].split(',')
        sections_start = f[34].split(',')
        t['sections'] = [ (float(start), float(conf)) \
            for start, conf in zip(sections_start, sections_confidence) if len(start) > 0 ]

        seg_confidence = f[35].split(',')
        seg_loudness_max = f[36].split(',')
        seg_loudness_max_time = f[37].split(',')
        seg_loudness_max_start = f[38].split(',')
        seg_pitches = f[39].split(',')
        seg_start = f[40].split(',')
        seg_timbre = f[41].split(',')

        PITCH_COUNT = 12
        TIMBRE_COUNT = 12
        t['segments'] = []
        for i, sstart in enumerate(seg_start):
            if len(sstart) > 0:
                seg = {}
                seg['start'] = float(sstart)
                seg['confidence'] = float(seg_confidence[i])
                seg['loudness_max'] = float(seg_loudness_max[i])
                seg['loudness_max_time'] = float(seg_loudness_max_time[i])
                seg['loudness_max_start'] = float(seg_loudness_max_start[i])
                seg['pitch'] =[ float(p) for p in seg_pitches[i * PITCH_COUNT: i * PITCH_COUNT + PITCH_COUNT]]
                seg['timbre'] =[ float(p) for p in seg_timbre[i * TIMBRE_COUNT: i * TIMBRE_COUNT + TIMBRE_COUNT]]
                t['segments'].append(seg)

        t['similar_artists'] = [s for s in f[42].split(',') if len(s) > 0]
        t['song_hotttnesss'] = float(f[43])
        t['song_id'] = f[44]
        t['start_of_fade_out'] = float(f[45])

        tatums_confidence = f[46].split(',')
        tatums_start = f[47].split(',')
        t['tatums'] = [ (float(start), float(conf)) \
            for start, conf in zip(tatums_start, tatums_confidence) if len(start) > 0 ]
        t['tempo'] = float(f[48])
        t['time_signature'] = (int(f[49]), float(f[50]))
        t['title'] = f[51]
        t['track_7digitalid'] = int(f[52])
        t['preview'] = 'http://previews.7digital.com/clips/34/%d.clip.mp3' % (int(f[52]), )
        t['year'] = int(f[53])
        return t
    else:
        print 'mismatched fields, found', len(f), 'should have 54'
        return None




def load_tracks(path):
    """ Loads a list of track from a file """

    tracks = []
    file = open(path)
    for which, line in enumerate(file):
        track = load_track(line)
        if track <> None:
            track['path'] = path
            track['line'] = which
            tracks.append(track)
    file.close()
    return tracks

def process_tracks(path, func):
    """ applies func(track) to each track found in path  """
    file = open(path)
    for which, line in enumerate(file):
        track = load_track(line)
        if track <> None:
            track['path'] = path
            track['line'] = which
            func(track)
    file.close()


def dump(track):
    """ Dumps some data from a track for debugging """
    print track['line'], track['track_id'], track['artist_id'],  len(track['artist_mbtags']), \
        len(track['artist_terms'] ), len(track['bars']), len(track['beats']), track['title'], \
        track['key'], track['mode'], len(track['segments'])


if __name__ == '__main__':
    process_tracks(sys.argv[1], dump)
