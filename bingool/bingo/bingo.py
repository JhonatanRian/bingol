import gc
from datetime import datetime
from random import randint, shuffle
from typing import List, Tuple
from threading import Thread


class Ball():

    def __init__(self: object, number: int) -> None:
        self.__number: int = number
        self.__drawn: bool = False

    @property
    def number(self: object) -> int:
        return self.__number

    @property
    def drawn(self: object) -> bool:
        return self.__drawn

    @drawn.setter
    def drawn(self: object, drawn: bool = True) -> None:
        self.__drawn = drawn

    def __repr__(self: object) -> str:
        return f"<ball {self.__number} {self.__drawn}>"

    def __str__(self: object) -> str:
        return f"Ball({self.__number})"

class Card():

    def __init__(self: object, uuid, line_1, line_2, line_3) -> None:
        self.__uuid: int = uuid
        self.__line1: List[Ball] = [Ball(n) for n in line_1]
        self.__line2: List[Ball] = [Ball(n) for n in line_2]
        self.__line3: List[Ball] = [Ball(n) for n in line_3]
        self.line1_win: bool = False
        self.line2_win: bool = False
        self.line3_win: bool = False

    @property
    def uuid(self: object):
        return self.__uuid

    def ball_drawn(self: object, number: int) -> None:
        for ball in self.__line1:
            if ball.number == number:
                ball.drawn = True
        for ball in self.__line2:
            if ball.number == number:
                ball.drawn = True
        for ball in self.__line3:
            if ball.number == number:
                ball.drawn = True
        self.line1_win = self.very_award(self.__line1)
        self.line2_win = self.very_award(self.__line2)
        self.line3_win = self.very_award(self.__line3)

    def very_award(self: object, line) -> bool:
        count = 0
        for ball in line:
            if ball.drawn:
                count += 1
        if count == 5:
            return True
        
        return False


    def __repr__(self: object) -> str:
        return f"{[self.__line1, self.__line2, self.__line3]}"


class Bingo():
    
    def __init__(self: object) -> None:
        self.__consummated: bool = False
        self.__results: dict = {}
        self.__balls: List[Ball] = [Ball(x) for x in range(1, 91)]
        self.__balls_drawn: List[Ball] = []
        self.__cards: List[Card] = []
        self.__cards_uuids: List[int] = []
        self.__standby: bool = None
        self.__cards_win_line: List[Card] = []
        self.__cards_win_line2: List[Card] = []
        self.__cards_win_bingo: List[Card] = []
        self.__cards_win_bingo2: List[Card] = []
        self.__cards_win_bingo3: List[Card] = []

    @property
    def balls_drawn(self: object) -> List[Ball]:
        return self.__balls_drawn

    @property
    def balls(self: object) -> List[Ball]:
        return self.__balls
    
    @property
    def results(self: object) -> dict:
        return self.__results

    @property
    def standby(self: object) -> bool:
        return self.__standby

    @property
    def cards(self: object) -> List[Card]:
        return self.__cards

    @property
    def cards_uuids(self: object) -> List[Card]:
        return self.__cards_uuids

    @property
    def cards_winners_line(self: object) -> List[Card]:
        return self.__cards_win_line

    @property
    def cards_winners_line2(self: object) -> List[Card]:
        return self.__cards_win_line2

    @property
    def cards_winners_bingo(self: object) -> List[Card]:
        return self.__cards_win_bingo

    @property
    def cards_winners_bingo2(self: object) -> List[Card]:
        return self.__cards_win_bingo2

    @property
    def cards_winners_bingo3(self: object) -> List[Card]:
        return self.__cards_win_bingo3

    @property
    def drawn_time(self: object) -> datetime:
        return self.__drawn_time

    @cards.setter
    def cards(self: object, card: Card) -> None:
        if self.__consummated:
            raise Exception("bingo consumed")
        
        self.__cards.append(card)

    @cards_uuids.setter
    def cards_uuids(self: object, _id: int) -> None:
        if self.__consummated:
            raise Exception("bingo consumed")

        self.__cards_uuids.append(_id)

    @standby.setter
    def standby(self: object, s: bool) -> None:
        if self.__consummated:
            raise Exception("bingo consumed")

        self.__standby = s

    def drawn(self: object) -> None:
        if self.__consummated:
            raise Exception("bingo consumed")

        shuffle(self.__balls)
        ball_drawn: Ball = self.__balls[randint(0, len(self.__balls) - 1)]
        ball_drawn: Ball = self.__balls.pop(self.__balls.index(ball_drawn))
        ball_drawn.drawn = True
        self.__balls_drawn.append(ball_drawn)
        self.cards_operations_drawn(ball_drawn.number)  
        return ball_drawn.number

    def cards_operations_drawn(self: object, number: int) -> None:
        if self.__consummated:
            raise Exception("bingo consumed")

        func = lambda c, n: c.ball_drawn(n)
        threads = [Thread(target=func, args=(card, number)) for card in self.__cards]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

    def cards_winners(self: object) -> tuple:
        if self.__consummated:
            raise Exception("bingo consumed")
        
        cards_winners: List[Tuple[Card, str]] = []

        threads = [Thread(target=self.verify_cards_winners, args=(card, cards_winners,)) for card in self.__cards]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        [self.increment_cards_winners(card) for card in cards_winners]

        return tuple(cards_winners)

    def verify_cards_winners(self, card: Card, cards_winners: list):    
        line1_win: bool = card.line1_win
        line2_win: bool = card.line2_win
        line3_win: bool = card.line3_win

        if not self.__cards_win_line:
            if any([line1_win, line2_win,line3_win]):
                cards_winners.append((card, "l1"))
        elif not self.__cards_win_line2:
            if all([line1_win, line2_win]) or all([line1_win, line3_win]) or all([line2_win, line3_win]):
                cards_winners.append((card, "l2"))
        elif not self.__cards_win_bingo:
            if all([line1_win, line2_win, line3_win]):
                cards_winners.append((card, "b1"))
        elif not self.__cards_win_bingo2:
            if all([line1_win, line2_win, line3_win]):
                cards_winners.append((card, "b2"))
        elif not self.__cards_win_bingo3:
            if all([line1_win, line2_win, line3_win]):
                cards_winners.append((card, "b3"))

    def increment_cards_winners(self: object, card):
        op: str = card[1]
        if op == "l1":
            self.__cards_win_line.append(card[0])
        elif op == "l2":
            self.__cards_win_line2.append(card[0])
        elif op == "b1":
            self.__cards_win_bingo.append(card[0])
        elif op == "b2":
            self.__cards_win_bingo2.append(card[0])
        elif op == "b3":
            self.__cards_win_bingo3.append(card[0])

    def generate_results(self: object) -> dict:
        if self.__consummated:
            raise Exception("bingo consumed! Use Bingo.results")

        res: list = []
        while len(self.balls_drawn) < 90:
            num_drawn: int = self.drawn()
            winners: List[Tuple[Card, str]] = self.cards_winners()
            res.append(
                {
                    'num_draw': num_drawn,
                    'winners': [{
                        'id': winner[0].uuid,
                        'initials': winner[1]
                    } for winner in winners]
                }
            )
        self.__consummated = True
        self.__results = res
        return res

if __name__ == "__main__":
    b = Bingo()
    b.cards = Card(1241417216728416724174687164871264, [12,35,42,59,65], [14,39,45,70,88], [12,45,66,73,86])
    b.cards = Card(124141721672841672417468716487126454576745773246634753573747373, [15,55,62,79,85], [24,49,55,60,78], [21,54,67,76,89])
    b.standby = False
    b.generate_results()
    from pprint import pprint
    pprint(b.results)