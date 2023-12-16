import sys
from collections import defaultdict
from functools import cmp_to_key

DAY = '07'
mode = sys.argv[1]
infile = f"./input/{DAY}_{mode}.txt"

HANDTYPES = {'5K': '7', 
             '4K': '6', 
             'FH': '5', 
             '3K': '4', 
             '2P': '3', 
             '1P': '2', 
             'HC': '1'}

CARDVALS = {'A': '14',
            'K': '13',
            'Q': '12',
            'J': '11',
            'T': '10'}

def typeHand(hand, jokerize=False):
    counted = defaultdict(int)
    for c in hand:
        counted[c] += 1
    if jokerize:
        assignJokers(counted)
    clen = len(counted.keys())
    if clen == 1:
        return '5K'
    if clen == 2:
        return '4K' if 4 in counted.values() else 'FH'
    if clen == 3:
        return '3K' if 3 in counted.values() else '2P'
    return '1P' if clen == 4 else 'HC'

def assignJokers(counted):
    j = counted.get('J', 0)
    # No jokers or all jokers, the result will be the same
    if j == 0 or j == 5:
        return counted
    # Remove the jokers from the hand
    del counted['J']
    # Reassign them to the biggest pot
    potsizes = sorted(counted.values(), reverse=True)
    if len(potsizes) > 1 and potsizes[0] == potsizes[1]:
        # We have to order the biggest pots by card and add the jokers there.
        cand = [x for x in counted.keys() if counted[x] == potsizes[0]] 
        cand.sort(reverse=True, key=lambda x: CARDVALS.get(x, x).zfill(2))
        # print(f"Turning {j} jokers into {cand[0]} cards")
        counted[cand[0]] += j
    else:
        # We can just add the jokers to the single biggest pot.
        for c in counted.keys():
            if counted[c] == potsizes[0]:
                # print(f"Turning {j} jokers into {c} cards")
                counted[c] += j
                break


def handSortVal(handtuple, jokerize=False):
    """Return a big digit string that can be used as a sort key."""
    hand = handtuple[0]
    s = [HANDTYPES[typeHand(hand, jokerize)]]
    cvals = [CARDVALS.get(x, x).zfill(2) for x in hand]
    s.extend(cvals)
    # print(f"Returning sort value {''.join(s)} for {hand}")
    return ''.join(s)

handset = []
with open(infile) as f:
    for l in f:
        handset.append(l.rstrip().split())

firstSort = sorted(handset, key=handSortVal)
secondSort = sorted(handset, key=lambda x: handSortVal(x, True))
firstTotal = 0
secondTotal = 0
for i, hs in enumerate(firstSort):
    firstTotal += (i+1) * int(hs[1])
print(f"Answer to part 1: {firstTotal}")
CARDVALS['J'] = '01'
for i, hs in enumerate(secondSort):
    secondTotal += (i+1) * int(hs[1])
print(f"Answer to part 2: {secondTotal}")
