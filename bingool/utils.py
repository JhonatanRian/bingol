from secrets import choice
from typing import List
from random import randint
from bingool.bingo.bingo import Card, Match
from bingool import models


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

def transform_simple_card(card, id_view: bool = False):
    simple_card = {}

    simple_card["id"] = card.id if id_view else None    
    simple_card["line1"] = [card.balls[index].number for index in range(5)]
    simple_card["line2"] = [card.balls[index].number for index in range(5, 10)]
    simple_card["line3"] = [card.balls[index].number for index in range(10,15)]

    return simple_card

def format_card(card):
    return Card(
        id_db=card.id,
            line_1=[ball.number for ball in card.line.all()[0].balls.all()],
            line_2=[ball.number for ball in card.line.all()[1].balls.all()],
            line_3=[ball.number for ball in card.line.all()[2].balls.all()]
        )

def keep_cards(b: Match , c: models.Card):
    c: Card = format_card(c)
    b.add_card(c)

if __name__ == "__main__":
    # print(create_line())
    # print(create_line())
    # print(create_line())
    # for i in range(10000):
    #     print(create_lines())
    print(create_lines())
    print(create_lines())
    print(create_lines())