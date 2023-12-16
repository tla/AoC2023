import re
import sys
from math import lcm

DAY = '08'
mode = sys.argv[1]
infile = f"./input/{DAY}_{mode}.txt"

path = None
routemap = dict()

# Get the input and make the map
with open(infile) as f:
    # First line is the path
    path = f.readline().rstrip()
    for line in f:
        m = re.match(r'(\w{3}) = \((\w{3}), (\w{3})\)', line)
        if m is not None:
            routemap[m.group(1)] = {'L': m.group(2), 'R': m.group(3)}

# Start with AAA and step until we find ZZZ
# print(routemap)
if 'AAA' in routemap:
    steps = 0
    pathpos = 0
    pos = 'AAA'
    while pos != 'ZZZ':
        steps += 1
        direction = path[pathpos]
        pathpos = (pathpos + 1) % len(path)
        pos = routemap[pos][direction]
    print(f"Answer to part 1: {steps}")

positions = [x for x in routemap.keys() if x.endswith('A')]
# The naive way that won't complete anytime soon
# steps = 0
# pathpos = 0
# while True:
#     # Check if we should break
#     zeds = [x for x in positions if x.endswith('Z')]
#     if len(positions) == len(zeds):
#         break
#     # Step as before
#     steps += 1
#     direction = path[pathpos]
#     pathpos += 1
#     if len(path) == pathpos:
#         pathpos = 0
#     positions = [routemap[x][direction] for x in positions]
#     print(f"Positions are now {positions}")

# Find the first Z-ending for each of our A-endings and then do some math
steps_to_z = dict()
for p in positions:
    if p in steps_to_z:
        continue
    steps = 0
    pathpos = 0
    pos = p
    while not pos.endswith('Z'):
        steps += 1
        direction = path[pathpos]
        pathpos = (pathpos + 1) % len(path)
        pos = routemap[pos][direction]
    steps_to_z[p] = steps

# now find the least common multiple of all our path lengths

print(f"Answer to part 2: {lcm(*steps_to_z.values())}")