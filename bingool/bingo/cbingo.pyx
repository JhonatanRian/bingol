from random import randint, shuffle
from threading import Thread
import cython


@cython.cclass
class Ball():
    __number: cython.int
    __drawn: cython.bint

    def __cinit__(self, number: cython.int):
        self.__number: cython.int = number
        self.__drawn: cython.bint = False

    @property
    def number(self) -> cython.int:
        return self.__number

    @property
    def drawn(self) -> cython.bint:
        return self.__drawn

    @drawn.setter
    def drawn(self, drawn: cython.bint) -> cython.void:
        self.__drawn = drawn

    def __repr__(self: object) -> str:
        return f"<ball {self.__number} {self.__drawn}>"

    def __str__(self: object) -> str:
        return f"Ball({self.__number})"


@cython.cclass
class Card():

    __uuid: int
    __line1: list
    __line2: list
    __line3: list
    line1_finalized: cython.bint
    line2_finalized: cython.bint
    line3_finalized: cython.bint
    type_award: str

    def __cinit__(self, uuid: int, line_1: list, line_2: list, line_3: list):
        self.__uuid = uuid
        self.__line1 = [Ball(n) for n in line_1]
        self.__line2 = [Ball(n) for n in line_2]
        self.__line3 = [Ball(n) for n in line_3]
        self.line1_finalized = False
        self.line2_finalized = False
        self.line3_finalized = False


    @property
    def uuid(self) -> cython.longlong:
        return self.__uuid

    @property
    def type_award(self) -> str:
        return self.type_award

    @cython.returns(cython.void)
    def ball_drawn(self, number: cython.int) -> cython.void:
        for ball in self.__line1:
            if ball.number == number:
                ball.drawn = True
        for ball in self.__line2:
            if ball.number == number:
                ball.drawn = True
        for ball in self.__line3:
            if ball.number == number:
                ball.drawn = True

        if not self.line1_finalized:
            self.line1_finalized = self.very_award(self.__line1)
        if not self.line2_finalized:
            self.line2_finalized = self.very_award(self.__line2)
        if not self.line3_finalized:
            self.line3_finalized = self.very_award(self.__line3)

        self.define_award([self.line1_finalized, self.line2_finalized, self.line3_finalized])

    @cython.returns(cython.bint)
    def very_award(self, line: list) -> cython.bint:
        count: cython.int = 0
        for ball in line:
            if ball.drawn:
                count += 1
        if count == 5:
            return True
        
        return False

    @cython.returns(cython.void)
    def define_award(self, lines_list: list):
        cont = len([line for line in lines_list if line])
        if cont == 1:
            self.type_award = "l1"
        elif cont == 2:
            self.type_award = "l2"
        elif cont == 3:
            self.type_award = "b"



    def __repr__(self) -> str:
        return f"{[self.__line1, self.__line2, self.__line3]}"


@cython.cclass
class Bingo():
    
    __consummated: cython.bint
    __results: list[dict]
    __balls: list[Ball]
    __balls_drawn: list[Ball]
    __cards: list[Card]
    __cards_uuids: list[int]
    __standby: cython.bint
    __cards_win_line: list[Card]
    __cards_win_line2: list[Card]
    __cards_win_bingo: list[Card]
    __cards_win_bingo2: list[Card]
    __cards_win_bingo3: list[Card]
    __drawn: cython.int
    __lucky_ball_winners: list[Card]

    def __cinit__(self):
        self.__consummated = False
        self.__drawn = 0
        self.__results = []
        self.__balls = [Ball(x) for x in range(1, 91)]
        self.__balls_drawn = []
        self.__cards = []
        self.__cards_uuids = []
        self.__standby = True
        self.__lucky_ball_winners = []
        self.__cards_win_line = []
        self.__cards_win_line2 = []
        self.__cards_win_bingo = []
        self.__cards_win_bingo2 = []
        self.__cards_win_bingo3 = []


    @property
    def consummated(self) -> cython.bint:
        return self.__consummated

    @property
    def balls_drawn(self) -> list[Ball]:
        return self.__balls_drawn

    @property
    def drawn(self) -> cython.int:
        return self.__drawn

    @property
    def balls(self) -> list[Ball]:
        return self.__balls
    
    @property
    def results(self) -> dict:
        return self.__results

    @property
    def standby(self) -> cython.bint:
        return self.__standby

    @property
    def cards(self) -> list[Card]:
        return self.__cards

    @property
    def cards_uuids(self) -> list[Card]:
        return self.__cards_uuids

    @property
    def cards_winners_line(self) -> list[Card]:
        return self.__cards_win_line

    @property
    def cards_winners_line2(self) -> list[Card]:
        return self.__cards_win_line2

    @property
    def cards_winners_bingo(self) -> list[Card]:
        return self.__cards_win_bingo

    @property
    def cards_winners_bingo2(self) -> list[Card]:
        return self.__cards_win_bingo2

    @property
    def cards_winners_bingo3(self) -> list[Card]:
        return self.__cards_win_bingo3

    @property
    def lucky_ball_winners(self) -> list[Card]:
        return self.__lucky_ball_winners

    @cards.setter
    def cards(self, card: Card) -> cython.void:
        if self.__consummated:
            raise Exception("bingo consumed")

        self.__cards.append(card)
        self.__cards_uuids.append(card.uuid)


    @standby.setter
    def standby(self, s: cython.bint) -> cython.void:
        if self.__consummated:
            raise Exception("bingo consumed")

        self.__standby = s
    
    @cython.returns(cython.int)
    def drawn_ball(self, num_draw: cython.int = 0) -> cython.int:
        if self.__consummated:
            raise Exception("bingo consumed")

        if not num_draw:
            self.__lucky_ball_winners.clear()
            shuffle(self.__balls)
            ball_drawn: Ball = self.__balls[randint(0, len(self.__balls) - 1)]
            ball_drawn: Ball = self.__balls.pop(self.__balls.index(ball_drawn))
        else:
            ball_drawn: Ball = [ball for ball in self.__balls if ball.number == num_draw][0]
        ball_drawn.drawn = True
        self.__drawn = ball_drawn.number
        self.__balls_drawn.append(ball_drawn)
        self.cards_operations_drawn(ball_drawn.number)
        return ball_drawn.number

    @cython.returns(cython.void)
    @cython.cfunc
    def cards_operations_drawn(self, number: cython.int) -> cython.void:
        if self.__consummated:
            raise Exception("bingo consumed")

        threads = [Thread(target=self.func, args=(self, card, number,)) for card in self.__cards]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        [self.increment_cards_winners(card) for card in self.__lucky_ball_winners]
    
    @cython.cfunc
    def func(self, c: Card, n: cython.int) -> cython.void:
        c.ball_drawn(n)
        self.verify_card_winners(c)

    @cython.returns(cython.void)
    @cython.cfunc
    def verify_card_winners(self, card: Card) -> cython.void:

        if not self.__cards_win_line:
            if card.type_award == "l1":
                self.__lucky_ball_winners.append((card, "l1"))
        elif not self.__cards_win_line2:
            if card.type_award == "l2":
                self.__lucky_ball_winners.append((card, "l2"))
        elif not self.__cards_win_bingo:
            if card.type_award == "b":
                self.__lucky_ball_winners.append((card, "b1"))
        elif not self.__cards_win_bingo2:
            if card.type_award == "b":
                self.__lucky_ball_winners.append((card, "b2"))
        elif not self.__cards_win_bingo3:
            if card.type_award == "b":
                self.__lucky_ball_winners.append((card, "b3"))

    @cython.returns(cython.void)
    @cython.cfunc
    def increment_cards_winners(self, card: tuple) -> cython.void:
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


    @cython.returns(cython.void)
    def generate_results(self) -> cython.void:
        if self.__consummated:
            raise Exception("bingo consumed! Use Bingo.results")
        if self.__standby:
            raise Exception("in standby")

        res: list = []
        while len(self.balls_drawn) < 90:
            num_drawn: int = self.drawn_ball()
            winners: list = self.lucky_ball_winners
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