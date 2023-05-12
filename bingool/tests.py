# from django.test import TestCase

# Create your tests here.
from bingo.factory import *
from random import randint, choice
nuns_drawn = []
def create_line(num_balls: int = 9, num_col: int = 5, no_repeat=False) -> List[int]:
    coluns_candidates = [[end :=(number*9)+number, end - 9][::-1] for number in range(1, num_balls+1)]
    line = []
    global nuns_drawn

    for i in range(num_col):
        interval = coluns_candidates.pop(randint(0, len(coluns_candidates) - 1))
        number = choice([x for x in range(interval[0], interval[1]) if not (x in nuns_drawn)])
        if no_repeat:
            nuns_drawn.append(number)
        line.append(number)
    line.sort()
    return line

def create_lines(num_lines: int = 3, num_balls: int = 9, num_col: int = 5):
    lines = []
    for line in range(num_lines):
        lines.append(create_line(num_balls=num_balls, num_col=num_col, no_repeat=True))
    nuns_drawn.clear()
    return lines

globe = globe()
match: Match = match()
for i in range(1, 500):
	lines = create_lines()
	c = Card(i, lines[0], lines[1], lines[2])
	match.add_card(c)

# for i in range(45):
# 	globe.drawn_ball()
c = 0
for round in match:
	c += 1
	if c >= 80:
		...
	print(round)
print()
# print(globe)
# print(next(match))
# print(match.cards)
# print()