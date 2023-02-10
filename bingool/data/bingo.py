from bingool.models import Bingo, Bot
from bingool.data.ball import RepositoryBall as rball


class RepositoryBingo:

    @classmethod
    def create(cls: type) -> Bingo:
        bingo_model = Bingo.objects.create(color=None, ball_drawn=None)
        return bingo_model

    @classmethod
    def get(cls: type) -> Bingo:
        return Bingo.objects.all().exists()

    @classmethod
    def create_bot(cls: type) -> Bingo:
        bot = Bot.objects.create()
        return bot

    @classmethod
    def get_bot(cls: type) -> Bingo:
        bot = Bot.objects.all().first()
        return bot

    @classmethod
    def standby(cls: type, standby: bool) -> None:
        Bingo.objects.filter(pk=1).update(standby=standby)

    @classmethod
    def reset(cls: type) -> None:
        Bingo.objects.filter(pk=1).update(
            standby=False,
            color=None,
            ball_drawn=None
        )
           
        rball.reset()

    @classmethod
    def bingo_drawn(cls: type, ball_drawn: int, color: str) -> None:
        Bingo.objects.filter(pk=1).update(
            ball_drawn=ball_drawn,
            color=color
        )
