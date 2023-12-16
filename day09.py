import sys

DAY = '09'
mode = sys.argv[1]
infile = f"./input/{DAY}_{mode}.txt"

def get_gaps(sequence):
    gaps = []
    for i, n in enumerate(sequence):
        if i == 0:
            continue
        gaps.append(n - sequence[i-1])
    return gaps

def infer_next(sequence):
    gaps = get_gaps(sequence)
    gs = set(gaps)
    if len(gs) == 1 and 0 in gs:
        # We have reached the bottom
        return sequence[-1]
    else:
        return sequence[-1] + infer_next(gaps)
    
def infer_prior(sequence):
    gaps = get_gaps(sequence)
    gs = set(gaps)
    if len(gs) == 1 and 0 in gs:
        return sequence[0]
    else:
        return sequence[0] - infer_prior(gaps)

t1 = 0
t2 = 0
with open(infile) as f:
    for l in f:
        sequence = [int(x) for x in l.rstrip().split()]
        t1 += infer_next(sequence)
        t2 += infer_prior(sequence)

print(f"Answer to part 1: {t1}")
print(f"Answer to part 2: {t2}")