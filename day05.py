import queue
import re
import sys
from datetime import datetime
from functools import reduce
from multiprocessing import Process, Queue

DAY = '05'

class LookupMap:
    def __init__(self, line):
        m = re.match(r'(\w+)-to-(\w+) map:', line)
        if m is not None:
            self.srcname = m.group(1)
            self.trgname = m.group(2)
            self.maps = []
        else:
            print(f"WARNING: could not initialize map from input {line}")
    
    def add_spec(self, line):
        m = re.match(r"(\d+)\s+(\d+)\s+(\d+)", line)
        if m is not None:
            self.maps.append(tuple(int(x) for x in m.groups()))
        else:
            print(f"WARNING: could not add spec from input {line}")

    def lookup(self, input):
        # Step through the maps seeing if the input is in range
        for map in self.maps:
            (t, s, r) = map
            if input >= s and input < s + r:
                # We have a hit
                offset = input - s
                return t + offset
        # If we get this far, return the input number itself
        return input


def pinball(numrange, mapset, aq):
    print(f"{datetime.now()}: Checking range {numrange}")
    thismin = None
    for s in range(*numrange):
        thisrun = reduce(lambda x,y: y.lookup(x), mapset, s)
        if thismin is None or thismin > thisrun:
            thismin = thisrun
    print(f"{datetime.now()}: Adding {thismin} to queue for {numrange}")
    aq.put(thismin)


if __name__ == '__main__':
    mode = sys.argv[1]
    infile = f"./input/{DAY}_{mode}.txt"
    seeds = []
    seedranges = []
    mapsequence = []
    with open(infile) as f:
        currmap = None
        for l in f:
            line = l.rstrip()
            if len(seeds) == 0:
                # First line
                seeds = [int(x) for x in line.lstrip('Seeds: ').split()]
                for i in range(0, len(seeds), 2):
                    seedranges.append((seeds[i], seeds[i] + seeds[i+1]))
                print(f"Starting with seeds {seeds}")
                print(f"and seed ranges {seedranges}")
            elif line.endswith('map:'):
                # We are about to parse a new map; save the old map
                if currmap is not None:
                    mapsequence.append(currmap)
                currmap = LookupMap(line)
            elif line != '':
                # Assume it is a line of numbers
                currmap.add_spec(line)
        # Add the last map
        if currmap is not None:
            mapsequence.append(currmap)
    # Now run the seeds through the sequence of maps
    lastrun = reduce(lambda x,y: [y.lookup(j) for j in x], mapsequence, seeds)
    print(f"Answer to part 1: {min(lastrun)}")
    procs = []
    answers = Queue()
    for sr in seedranges:
        proc = Process(target=pinball, args=(sr, mapsequence, answers))
        procs.append(proc)
        proc.start()
    # Wait for all the processes to complete
    for proc in procs:
        proc.join()
    # Look at the answers
    rangerun = []
    while True:
        try:
            a = answers.get_nowait()
        except queue.Empty:
            break
        else:
            rangerun.append(a)

    print(f"Answer to part 2: {min(rangerun)}")