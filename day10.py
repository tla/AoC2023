import sys
from copy import deepcopy

DAY = '10'
mode = sys.argv[1]
infile = f"./input/{DAY}_{mode}.txt"


def advance(grid, step, p1, p2):
    max_i = len(grid) - 1
    max_j = len(grid[0]) - 1
    if step > max_i * max_j:
        raise Exception(f"Step count {step} exceeds {max_i} * {max_j}")
    nextsteps = []
    cp = None
    if step == 0:
        # Find the S, put a zero there, and return the first two positions
        for i, row in enumerate(grid):
            try:
                j = row.index('S')
                row[j] = step
                cp = ('S', i, j)
                # print(f"Starting with S at {(i,j)}")
                break
            except ValueError:
                continue
    else:
        # Put the current step number at the positions we reached
        # print(f"Starting at {p1} and {p2}")
        for pos in [p1, p2]:
            grid[pos[1]][pos[2]] = step

    # Now figure out what are the next positions we should be looking at
    for pos in [cp, p1, p2]:
        if pos is None:
            continue
        v, i, j = pos
        # Look to the top
        if i > 0 and v in ['J', 'L', '|', 'S'] and grid[i-1][j] in ['|', 'F', '7']:
            nextsteps.append((grid[i-1][j],i-1,j))
        # Look left
        if j > 0 and v in ['J', '7', '-', 'S'] and grid[i][j-1] in ['F', 'L', '-']:
            nextsteps.append((grid[i][j-1],i,j-1))
        # Look right
        if j < max_j and v in ['F', 'L', '-', 'S'] and grid[i][j+1] in ['J', '7', '-']:
            nextsteps.append((grid[i][j+1],i,j+1))
        # Look down
        if i < max_i and v in ['F', '7', '|', 'S'] and grid[i+1][j] in ['J', 'L', '|']:
            nextsteps.append((grid[i+1][j],i+1,j))

    # print(f"Next steps are {nextsteps}")
    return nextsteps


def inner_positions(slice, solved):
    ipset = []
    inside = False
    lastcorner = None
    for i, t in enumerate(solved):
        if type(t) == int:
            piece = slice[i]
            if piece in ['F', 'L']:
                lastcorner = piece
            elif piece == '|' or (piece == 'J' and lastcorner != 'L') or (piece == '7' and lastcorner != 'F'):
                lastcorner = None
                inside = not inside
            elif piece == 'S':
                lastcorner = 'F'
        elif inside:
            ipset.append(i)
    print(f"Marked tiles {ipset} from slice {slice} / {solved}")
    return ipset


grid = []
with open(infile) as f:
    for l in f:
        grid.append(list(l.rstrip()))

original = deepcopy(grid)
step = 0
nextsteps = [None, None]
seen = set()
while True:
    nextsteps = advance(grid, step, *nextsteps)
    step += 1
    if nextsteps[0] == nextsteps[1]:
        lst = nextsteps[0]
        grid[lst[1]][lst[2]] = step
        break
    for ns in nextsteps:
        if ns in seen:
            print(f"ERROR: spinning in a loop at {ns}")
            break
    seen.update(nextsteps)

print(f"Answer to part 1: {step}")

# Now we have to count tiles that are inside the loop.
inner_horizontal = set()
inner_vertical = set()

for i, row in enumerate(original):
    solved = grid[i]
    inner_horizontal.update([(i,x) for x in inner_positions(row, solved)])


print(f"Answer to part 2: {len(inner_horizontal)}")