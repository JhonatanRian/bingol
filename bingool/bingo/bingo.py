from random import randint, shuffle
from typing import List, Tuple
from threading import Thread
from dataclasses import dataclass, field
from typing import Optional, Callable

@dataclass(slots=True)
class Ball:
    number: int
    drawn: bool = field(default=False)

    def __eq__(self, other):
        if isinstance(other, Ball):
            return self.number == other.number
        return False


@dataclass(slots=True)
class Winner:
    award: 'Award'
    card: 'Card'


@dataclass(slots=True)
class Round:
    num_drawn: int
    winners: Optional[list[Winner]]
    ball_drawn: Ball


@dataclass(slots=True)
class Award:
    name: str
    rule: Callable[['Card'], Optional[Winner]] = field(repr=False)
    inactivate_card: bool = field(default=False, repr=False)
    amount_of_winners: int = field(default=1, repr=False)
    sub_prizes_obtained: int = field(default=0, repr=False)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return False


class Globe:
    def __init__(self, max_length):
        self.__balls: list[Ball] = [Ball(num) for num in range(1, max_length + 1)]
        self.__balls_drawn: list[Ball] = []

    @property
    def balls(self) -> list[Ball]:
        return self.__balls

    @property
    def balls_drawn(self) -> list[Optional[Ball]]:
        return self.__balls_drawn

    def rotate(self):
        for i in range(1, 3):
            shuffle(self.__balls)

    def drawn_ball(self):
        self.rotate()
        ball_drawn: Ball = self.__balls[randint(0, len(self.__balls) - 1)]
        ball_drawn: Ball = self.__balls.pop(self.__balls.index(ball_drawn))
        ball_drawn.drawn = True
        self.__balls_drawn.append(ball_drawn)
        return ball_drawn

    def __repr__(self):
        return f"<Globe balls: {len(self.balls)}, balls_drawn: {len(self.balls_drawn)}>"


class Card:

    def __init__(self, id_db: int, line_1: list[Ball], line_2: list[Ball], 
                 line_3: list[Ball]) -> None:
        self.__id: int = id_db
        self.__line1: List[Ball] = [Ball(n) for n in line_1]
        self.__line2: List[Ball] = [Ball(n) for n in line_2]
        self.__line3: List[Ball] = [Ball(n) for n in line_3]
        self.line1_win: bool = False
        self.line2_win: bool = False
        self.line3_win: bool = False
        self.__match: Optional['Match'] = None

    @property
    def id(self):
        return self.__id

    @property
    def line1(self):
        return self.__line1
    
    @property
    def line2(self):
        return self.__line2
    
    @property
    def line3(self):
        return self.__line3

    @property
    def match(self):
        return self.__match

    @match.setter
    def match(self, match: 'Match'):
        if self.match:
            raise("This Card is already in a game")
        self.__match = match

    def score_drawn_ball(self, ball_drawn: Ball) -> Optional['Card']:
        lines = [self.line1 + self.line2 + self.line3]
        line_to_consider: list[Optional[list]] = [line for line in lines if ball_drawn in line]
        
        if line_to_consider:
            line = line_to_consider[0]
            line[line.index(ball_drawn)].drawn = True

            self.line1_win = all([ball.drawn for ball in self.line1])
            self.line2_win = all([ball.drawn for ball in self.line2])
            self.line3_win = all([ball.drawn for ball in self.line3])
            
            self.__recognize_victory()
        return self

    def __recognize_victory(self) -> None:
        for award in self.match.awards:
            if winner := award.rule(self, award):
                print('\n', winner, '\n')
                if winner.award.inactivate_card:
                    self.match.inactivate_card(self)
                self.match.listen_card(winner)
                self.match.prizes_obtained_round = award.name


    def __repr__(self) -> str:
        return f"<Card {self.id}, {self.line1_win}, {self.line2_win}, {self.line3_win}>"
        # return f"<Card line1_win: {self.line1_win}, line2_win: {self.line2_win}, line3_win: {self.line3_win}>"


class Match:
    def __init__(self, awards: list[Award], globe: Globe):
        self.__cards: list[Card] = []
        self.__cards_winning = []
        self.__cards_without_played: list[Optional[Card]] = []
        self.__awards: list[Award] = awards
        self.__award_used: list[Optional[Award]] = []
        self.__globe: Globe = globe
        self.__rounds: list[Round] = []
        self.__prizes_obtained_round = []

    @property
    def cards(self) -> list[Card]:
        return self.__cards

    @property
    def globe(self) -> Globe:
        return self.__globe

    @property
    def awards(self) -> list[Award]:
        return self.__awards

    @property
    def rounds(self) -> list[Round]:
        return self.__rounds
    
    @property
    def prizes_obtained_round(self):
        return self.__prizes_obtained_round
    
    @prizes_obtained_round.setter
    def prizes_obtained_round(self, award_name: str):
        self.__prizes_obtained_round.append(award_name)

    def add_card(self, card: Card):
        self.__cards.append(card)
        card.match = self

    def listen_card(self, card: Card):
        self.__cards_winning.append(card)

    def inactivate_card(self, card: Card):
        self.__cards_without_played.append(card)

    def __change_award(self):
        if self.__cards_winning:
            # print(self.__award_used)
            # print(self.__cards_without_played)
            # print(self.cards)
            self.__prizes_obtained_round = list(set(self.__prizes_obtained_round))
            # print(self.__prizes_obtained_round)
            for name_award in self.__prizes_obtained_round:
                index_award = self.__awards.index(name_award)
                if self.__awards[index_award].amount_of_winners > 0:
                    continue
                self.__award_used.append(self.__awards.pop(index_award))
            self.__prizes_obtained_round.clear()


    def __warn_cards(self, ball: Ball):
        func = lambda c, b: c.score_drawn_ball(b)
        threads = [Thread(target=func, args=(card, ball)) for card in self.__cards]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

    def move_game(self) -> Round:
        if len(self.cards) == 0 or not self.__awards or not self.globe.balls:
            raise StopIteration
        ball_drawn = self.globe.drawn_ball()
        self.__warn_cards(ball_drawn)
        round_ = Round(
            num_drawn=len(self.__rounds)+1,
            winners=self.__cards_winning.copy(),
            ball_drawn=ball_drawn
            )
        self.__rounds.append(round)
        self.__change_award()
        self.__cards_winning.clear()
        
        return round_

    def __iter__(self) -> 'Match':
        return self

    def __next__(self) -> Round:
        return self.move_game()

    def __repr__(self):
        round = self.__rounds[-1] if self.rounds else 'Not Started'
        return f'<Match current_award: {self.current_award.name}, round: {round}>'


if __name__ == "__main__":
    b = Bingo()
    b.cards = Card(1241417216728416724174687164871264, [12,35,42,59,65], [14,39,45,70,88], [12,45,66,73,86])
    b.cards = Card(124141721672841672417468716487126454576745773246634753573747373, [15,55,62,79,85], [24,49,55,60,78], [21,54,67,76,89])
    b.standby = False
    b.generate_results()
    from pprint import pprint
    pprint(b.results)