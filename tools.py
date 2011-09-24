import math
import random
import time


def interpolate(xdata, ydata, points):
    results = []
    duration = xdata[-1]
    inc = duration / float(points)
    ctime = 0
    cindex = 0

    last_index = 0
    for i in xrange(points):
        for j in xrange(last_index, len(xdata) - 1):
            #print 'xd', xdata[j], xdata[j+1], ctime
            if ctime < xdata[j+1]:
                break
        last_index = j

        frac = (ctime - xdata[j]) / (xdata[j+1] - xdata[j])
        y = frac * (ydata[j+1] - ydata[j]) + ydata[j]
        #print 'ct', ctime, xdata[j], xdata[j+1]
        results.append(y)

        ctime += inc
    return results


def smooth(data, fsize=10):
    out = []
    filter = []
    # bug, make this be a centering filter
    for d in data:
        filter.append(d)
        if len(filter) > fsize:
            filter.pop(0)
        out.append( sum(filter) / len(filter))
    return out

def sample(data, size):
    results = []
    jump = float(len(data)) / float(size)
    for i in xrange(size):
        index = int(round(i * jump))
        index = min(len(data) - 1, index)
        results.append(data[index])
    return results

    
def normalize(data, range = 1):
    max_data = max(data)
    min_data = min(data)

    out = [ range * (x - min_data) / (max_data - min_data) for x in data]
    return out

def rnormalize(data, min_data = 0, max_data = 1, range = 1):
    data = clamp(data, min_data, max_data)
    out = [ range * (x - min_data) / (max_data - min_data) for x in data]
    return out


def clamp(data, min_data, max_data):
    results = []
    for d in data:
        d = min(d, max_data)
        d = max(d, min_data)
        results.append(d)
    return results


def distance(d1, d2):
    if len(d1) <> len(d2):
        raise ValueError
    sum = 0
    for p1, p2 in zip(d1, d2):
        d = p2 - p1
        dd = d * d
        sum += dd
        #print p1, p2, dd, sum
    return math.sqrt(sum)

def qdistance(d1, d2):
    if len(d1) <> len(d2):
        raise ValueError
    sum = 0
    for p1, p2 in zip(d1, d2):
        d = p2 - p1
        dd = d * d
        sum += dd
        #print p1, p2, dd, sum
    return sum

    

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



def sinwave(size):
    results = []
    inc = 3.14159 / size
    angle = 0
    for x in xrange(size):
        results.append( math.sin(angle) )
        angle += inc

    return normalize(results)

def sin2wave(size):
    results = []
    inc = 3.14159 / size
    angle = -3.14159/2
    for x in xrange(size):
        results.append( math.sin(angle) )
        angle += inc

    return normalize(results)

def sin3wave(size):
    results = []
    inc = 4 * 3.14159 / size
    angle = -3.14159/2
    for x in xrange(size):
        results.append( math.sin(angle) )
        angle += inc

    return normalize(results)

def coswave(size):
    results = []
    inc = 3.14159 / size
    angle = 0
    for x in xrange(size):
        results.append( math.cos(angle) )
        angle += inc

    return normalize(results)

def ramp(start = 0, inc = 1, size=10):
    results = []
    val = start
    for x in xrange(size):
        results.append( val )
        val += inc
    return results
  
def  add_noise(data, range):
    results = []
    for d in data:
        results.append(d + random.triangular(-range, range))
    return results

def  scale(data, scale, offset = 0):
    results = []
    for d in data:
        results.append(d * scale + offset)
    return results

def dump(d):
    for i in d:
        print i

def timing(size = 32,count = 1000000):
    start = time.time()
    sin2 = sin2wave(size)
    cos = coswave(size)

    for i in xrange(count):
       qdistance(sin2, cos)

    end = time.time()

    print end - start




def timing2(size = 32, count = 1000000):
    start = time.time()
    ramp1 = ramp(0, 1, size)
    ramp2 = ramp(0, 2, size)

    for i in xrange(count):
       qdistance(ramp1, ramp2)

    end = time.time()

    print end - start

def test():
    xdata = aamp(0, .3, 1000)
    ydata = sin2wave(1000)
    ydata = add_noise(ydata, .5)
    idata = interpolate(xdata, ydata, 1400)
    sdata = smooth(idata, 20)
    samp = sample(sdata, 256)
    ndata = normalize(samp)

    sin2 = sin2wave(256)
    cos = coswave(256)
    sin = sinwave(256)
    flat = normalize(ramp(0, .01, 256))

    print "# sin2wav", distance(ndata, sin2)
    print "# coswav", distance(ndata, cos)
    print "# sinwav", distance(ndata, sin)
    print "# flat", distance(ndata, flat)

    for i, (a, b, c, d, e) in enumerate(zip(ndata, sin2, cos, sin, flat)):
        print i, a,b,c,d,e



if __name__ == '__main__':
    #timing()
    #timing2()
    dump(sin3wave(100))
    #test()
