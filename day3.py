import re
import sys
from collections import defaultdict

DAY = '03'
mode = sys.argv[1]
infile = f"./input/{DAY}_{mode}.txt"

symbol_addresses = set()
symbol_adjacency = defaultdict(list)
star_addresses = set()

with open(infile) as f:
    lines = f.readlines()
    lines = [x.rstrip() for x in lines]

# Find all symbol addresses
for i, l in enumerate(lines):
    symbols = re.finditer(r'[^\d\.]', l)
    for m in symbols:
        saddr = (m.start(), i)
        symbol_addresses.add(saddr)
        if m.group(0) == '*':
            star_addresses.add(saddr)
# print(symbol_addresses)

# Find all numbers
partsum = 0
for i, l in enumerate(lines):
    numbers = re.finditer(r'\d+', l)
    for n in numbers:
        # Check the line above
        pn = int(n.group(0))
        toadd = 0
        for j in range(n.start()-1, n.end()+1):
            if (j, i-1) in symbol_addresses:
                toadd = pn
                symbol_adjacency[(j,i-1)].append(n)
            if (j, i+1) in symbol_addresses:
                toadd = pn
                symbol_adjacency[(j,i+1)].append(n)
        if (n.start()-1, i) in symbol_addresses:
            toadd = pn
            symbol_adjacency[(n.start()-1, i)].append(n)
        if (n.end(), i) in symbol_addresses:
            toadd = pn
            symbol_adjacency[(n.end(), i)].append(n)
        partsum += toadd
print(f"Answer for part 1: {partsum}")

# Now find the "gears"
ratio = 0
for gearsym in sorted(star_addresses):
    connected = symbol_adjacency.get(gearsym, [])
    if len(connected) == 2:
        # Get the two numbers, multiply them, and add them to the total
        n1 = int(connected[0].group(0))
        n2 = int(connected[1].group(0))
        # print(f"Multiplying {n1} and {n2}")
        ratio += n1 * n2
print(f"Answer for part 2: {ratio}")