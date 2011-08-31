from mrjob.job import MRJob
import track

class MRComplexity(MRJob):

    def mapper(self, _, line):
        t = track.load_track(line)
        if t:
            if t['tempo'] > 0:
                complexity = len(t['segments']) / t['duration']
                #only output extreme complexities
                if complexity > 8 or complexity < .5:
                    yield (t['artist_name'], t['title'], t['song_id']), complexity

    # no need for a reducer
    #def reducer(self, key, val):
        #yield (key, sum(val))

if __name__ == '__main__':
    MRComplexity.run()
