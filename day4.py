import re
import sys
from copy import deepcopy
from functools import reduce

DAY = '04'
mode = sys.argv[1]
infile = f"./input/{DAY}_{mode}.txt"

class Card:
    id = 0
    winners = set()
    held = set()
    matches = set()

    def __init__(self, line):
        m = re.match(r'Card\s+(\d+):\s+([\d ]+\d)\s+\|\s+([\d ]+\d)', line)
        if m is None:
            print(f"WARNING: Could not initialize card from {line}")
        else:
            self.id = int(m.group(1))
            self.winners = {int(x) for x in m.group(2).split()}
            self.held = {int(x) for x in m.group(3).split()}
            self.matches = self.winners.intersection(self.held)

    def score(self):
        if len(self.matches):
            return 2 ** (len(self.matches) - 1)
        else:
            return 0
        
    def copies(self, cardlist):
        # Given the whole list of cards, return the cards that should be
        # duplicated as won
        cardidx = {x.id:x for x in cardlist}
        copied = []
        for i in range(len(self.matches)):
            w = self.id + i + 1
            if w in cardidx:
                copied.append(deepcopy(cardidx[w]))
        return copied
    
    def __repr__(self) -> str:
        return f"Card {self.id}: winning matches {self.matches}"
    
    


with open(infile) as f:
    cards = [Card(l.rstrip()) for l in f]

# Score all the individual cards
pointsum = reduce(lambda x,y: x + y.score(), cards, 0)
print(f"Answer to part 1: {pointsum}")

# Add up all the card copies
outstanding = {x.id:1 for x in cards}
total = len(cards)
# Look at card 1, add a counter to outstanding for each card ID that is copied
for c in cards:
    won = c.copies(cards)
    times = outstanding[c.id]
    for n in won:
        outstanding[n.id] += times
    total += times * len(won)
    print(f"Processed card {c.id}, won {len(won)} more, outstanding {outstanding[c.id]} times, and total is now {total}")


print(f"Answer to part 2: {total}")