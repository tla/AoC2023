import sys

DAY = '11'
mode = sys.argv[1]
infile = f"./input/{DAY}_{mode}.txt"

def transform_coordinates(galaxies, padded_i, padded_j, factor):
    # Each galaxy coordinate has to expand by the factor for i or j less than its own coordinate
    expanded = []
    for g in galaxies:
        g_i, g_j = g
        for i in padded_i:
            if i < g[0]:
                g_i += factor - 1
        for j in padded_j:
            if j < g[1]:
                g_j += factor -1
        expanded.append((g_i, g_j))
    return expanded


def collect_distances(galaxies):
    # Sum up the distance between each pair of galaxies.
    total = 0
    for a in range(len(galaxies)):
        thisgal = galaxies[a]
        for b in range(a+1, len(galaxies)):
            thatgal = galaxies[b]
            distance = abs(thisgal[0] - thatgal[0]) + abs(thisgal[1] - thatgal[1])
            total += distance
    return total


universe = []
with open(infile) as f:
    for line in f:
        universe.append(list(line.rstrip()))

# Get the galaxy coordinates
galaxies = []
for i, row in enumerate(universe):
    for j in range(len(row)):
        if row[j] == '#':
            galaxies.append((i, j))

# See where we have to pad out empty rows
padded_i = []
for i, row in enumerate(universe):
    if '#' not in row:
        padded_i.append(i)

padded_j = []
for j in range(len(universe[0])):
    col = [row[j] for row in universe]
    if '#' not in col:
        padded_j.append(j)

brief = transform_coordinates(galaxies, padded_i, padded_j, 2)
huge = transform_coordinates(galaxies, padded_i, padded_j, 1000000)

print(f"Answer to part 1: {collect_distances(brief)}")
print(f"Answer to part 2: {collect_distances(huge)}")
