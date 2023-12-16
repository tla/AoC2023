import re
import sys

DAY = '01'
mode = sys.argv[1]
infile = f"./input/{DAY}_{mode}.txt"

words = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',

}

def numsearch(s):
    matches = re.finditer(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', s)
    return [match.group(1) for match in matches]

def lastdigit(val):
    return words.get(val, val)

a1 = 0
a2 = 0
with open(infile) as f:
    for line in f:
        num1 = re.findall('\d', line)
        num2 = numsearch(line)
        if len(num1):
            print(f"Found {num1} from {line.rstrip()}")
            a1 += int(''.join([num1[0], num1[-1]]))
        else:
            print(f"No digits found on line: {line.rstrip()}")
        if len(num2):
            print(f"Found {num2} from {line.rstrip()}")
            a2 += int(''.join([lastdigit(num2[0]), lastdigit(num2[-1])]))
        else:
            print(f"No numbers found on line: |{line.rstrip()}|")

print(f"Answer for part 1: {a1}")
print(f"Answer for part 2: {a2}")