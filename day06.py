import re
import sys
from math import sqrt, floor, ceil

DAY = '06'
mode = sys.argv[1]
infile = f"./input/{DAY}_{mode}.txt"

def quadratic(a, b, c):
    term = sqrt(b**2 - 4*a*c)
    a1 = (-b + term) / (2*a)
    a2 = (-b - term) / (2*a)
    return a1, a2

def quadratic_whole_range(a, b, c):
    (min, max) = quadratic(a, b, c)
    if ceil(min) == min:
        min = ceil(min) + 1
    else:
        min = ceil(min)
    if floor(max) == max:
        max = floor(max)
    else:
        max = floor(max) + 1
    return range(min, max)

def parseline(line, prefix):
    pattern = f"{prefix}:\\s+"
    return [int(x) for x in re.sub(pattern, '', line.rstrip()).split()]

with open(infile) as f:
    timeseries = parseline(f.readline(), 'Time')
    distseries = parseline(f.readline(), 'Distance')
    # Part 1: how many ways can we beat the record?
    total = 1
    for i, t in enumerate(timeseries):
        d = distseries[i]
        r = quadratic_whole_range(-1, t, -d)
        print(f"Time {t}, distance {d}; got range {r}")
        total = total * len(r)
    print(f"Answer to part 1: {total}")
    # Part 2: oops, it's actually a single huge number
    timebig = int(''.join([str(x) for x in timeseries]))
    distbig = int(''.join([str(x) for x in distseries]))
    rbig = quadratic_whole_range(-1, timebig, -distbig)
    print(f"Answer to part 2: {len(rbig)}")
