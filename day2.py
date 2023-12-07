import re
import sys
from functools import reduce

DAY = '02'
mode = sys.argv[1]
infile = f"./input/{DAY}_{mode}.txt"

maxcubes = {
    'red': 12,
    'green': 13,
    'blue': 14
}

gamesum = 0
powersum = 0
with open(infile) as f:
    for line in f:
        maxseen = {'red': 0, 'green': 0, 'blue': 0}
        [game, cubelist] = line.rstrip().split(': ')
        # This should match every time
        m = re.match(r'Game (\d+)', game)
        gnum = int(m.group(1))
        # Split the cubelist
        for display in cubelist.lstrip().split('; '):
            for amount in display.split(', '):
                m = re.match(r'(\d+) (red|green|blue)', amount)
                (cnum, color) = m.group(1, 2)
                c = int(cnum)
                if c > maxseen.get(color):
                    maxseen[color] = c
                if c > maxcubes.get(color):
                    # Set the game number to zero as a means of avoiding adding it
                    gnum = 0
        gamesum += gnum
        powersum += reduce(lambda x,y: x*y, maxseen.values())

print(f"Answer to part 1: {gamesum}")
print(f"Answer to part 2: {powersum}")