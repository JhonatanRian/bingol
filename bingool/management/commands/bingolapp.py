from django.core.management.base import BaseCommand
from gc import collect
from time import sleep
from bingool.bingo.bingo_application import BingoApplication
from bingool.data.match import RepositoryMatch as rmatch
from bingool.data.bingo import RepositoryBingo as rbingo
from bingool.data.ball import RepositoryBall as rball
from loguru import logger
from bingool.bingo import factory

class Command(BaseCommand):
    help = 'bot bingol'

    def handle(self, *args, **kwargs):
        # Implementation of the command

        if not rbingo.get():
            logger.info("criando bingo na API")
            bingo = rbingo.create()
            rball.create_balls(bingo)

        rbingo.reset()
    
        while True:
            collect()

            logger.info("procurando partida")

            if not (match := rmatch.get_match()):
                sleep(1)
            elif match.automatic:
                application: BingoApplication = BingoApplication(factory.match())

                application.init()

                rmatch.finish(match.id)
                sleep(6.5)
                del application
                collect()
            else:
                application: BingoApplication = BingoApplication()
                application.init(draw=False)
                rmatch.finish(match.id)
                sleep(6.5)
                del application
                collect()
