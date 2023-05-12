import gc
from random import choice
from threading import Thread
from time import sleep
from datetime import datetime
from bingool.utils import keep_cards
from loguru import logger
from bingool.data.ball import RepositoryBall as rball
from bingool.data.bingo import RepositoryBingo as rbingo
from bingool.data.card import RepositoryCard as rcard
from bingool.data.match import RepositoryMatch as rmatch
from bingool.data.winner import RepositoryWinner as rwinner
from bingool.data.award import RepositoryAward as raward
from collections import Counter
from bingool.models import Match, Card, Award, Bingo
from bingool.bingo import bingo


class BingoApplication:

    def __init__(self, match: bingo.Match) -> None:
        self.__match_model: Match = rmatch.get_match()
        self.awards = list(self.match_model.award.all())
        self.match: bingo.Match = match
        self.standby = True
        self.rounds: list[self.rounds] = []
        self.colors = ["color1", "color2", "color3", "color4", "color5", "color6", "color7", "color8", "color9"]

    @property
    def match_model(self) -> Match:
        return self.__match_model

    def insert_cards_in_bingo(self):
        resp_cards: list[Card] = rcard.get_all_new_cards()
        threads = [Thread(target=keep_cards, args=(self.match, card))
                   for card in resp_cards]
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        rcard.update_inlive_cards(resp_cards, self.match_model.id)

    def wait_and_saving(self, time: datetime):  
        time_left_seconds = (time - datetime.now()).seconds
        while time_left_seconds != 0:
            logger.info(F"capturando cartelas; TEMPO:{time_left_seconds}s")
            sleep(1)
            if (t := rmatch.get(self.__match_model.id).datetime_to_start) != time:
                time = t

            time_left_seconds = (time - datetime.now()).seconds

            if time_left_seconds == 30:
                rbingo.standby(False)
                self.insert_cards_in_bingo()

            if time_left_seconds == 0:
                self.standby = False


    def standby_process(self, time: datetime):
        rbingo.standby(True)

        thread = Thread(target=self.wait_and_saving, args=(time,))
        thread.start()
        while self.standby:
            ...

        rmatch.initiated(self.match_model.id)
        self.generate_results()
        thread.join()

    def generate_results(self):
        for round in self.match:
            self.rounds.append(round)

    def define_winners(self, winners: list[bingo.Winner]):
        list_award_won = Counter([x.award.name for x in winners])
        count_acc = 0

        for winner in winners:
            card_model: Card = rcard.get(winner.card.id)
            if winner.award.name == 'b1' and len(self.match.globe.balls_drawn) <= 38:
                count_acc += 1
            else:
                award: Award = list(
                    filter(lambda a: a.initials == winner.award.name, self.awards))[0]
            rwinner.create_winner(card_model.user_id, award.id, card_model.id,
                                  award.value / list_award_won[award.initials])

            for i in range(count_acc):
                award: Award = raward.get_accumulate()
                value = award.value / count_acc
                raward.create_award(name='accumulate', value=0, initials='ac')
                rwinner.create_winner(card_model.user_id,
                                      award.id, card_model.id, value)

    def run_bingo(self):
        rbingo.standby(True)
        for round in self.rounds:
            round: bingo.Round = round
            color = choice(self.colors)

            number_ball_dranw = round.ball_drawn

            winners: list[bingo.Winner] = round.winners

            rball.draw_true(number_ball_dranw.number)
            rbingo.bingo_drawn(number_ball_dranw.number, color)

            logger.info(f"bola: {number_ball_dranw.number} sorteada")
            if winners:
                self.define_winners(winners)
                logger.info(f"Temos {len(winners)} cartelas vencedoras")
                sleep(6)
                continue
            sleep(4)

        logger.info(
            "Deletando objetos, salvando resultados na partida e resetando bingo na API")
        rcard.update_finalized_all_cards(self.match_model.id)
        # rmatch.save_results(self.match_model.id, self.bingo.results)
        rbingo.reset()
        gc.collect()

    def bingo_raffling(self):

        logger.info("STANDBY")
        self.standby_process(self.match_model.datetime_to_start)

        logger.info("BINGO")
        sleep(7)
        self.run_bingo()

    def bingo_not_raffling(self):

        logger.info("STANDBY")
        self.standby_process(self.match_model.datetime_to_start)
        num_drawn = 0
        while True:
            while True:
                bingo_model: Bingo = rbingo.get()
                if bingo_model.ball_drawn != num_drawn:
                    num_drawn = bingo_model.ball_drawn
                    break
                else:
                    ...
            self.bingo.drawn_ball(num_drawn)
            if winners := [{'id': winner[0].uuid, 'initials': winner[1]} for winner in self.bingo.lucky_ball_winners]:
                self.define_winners(winners)
                if [winner for winner in winners if winner.get('initials') == 'b3']:
                    logger.info(
                        "Bingo finalizado. Todos os premios já foram conquistados")
                    break

    def init(self, draw: bool = True):
        if draw:
            self.bingo_raffling()
            return
        self.bingo_not_raffling()