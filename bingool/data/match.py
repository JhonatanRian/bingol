from bingool.models import Match
from json import dumps


class RepositoryMatch:

    @classmethod
    def get(cls: type, match_id: int) -> Match:
        return Match.objects.filter(pk=match_id).first()

    @classmethod
    def get_match(cls: type) -> Match:
        """"get_match" retorna a partida mais recente e ainda não finalizada "Match"

        Args:
            self (object): instância

        Returns:
            Match: ultimo elemento "Match" cadastro no db
        """
        return Match.objects.filter(finalized=False).order_by("datetime_to_start").first()

    @classmethod
    def finish(cls: type, match_id: int):
        Match.objects.filter(pk=match_id).update(
            finalized=True
        )

    @classmethod
    def initiated(cls: type, match_id: int):
        Match.objects.filter(pk=match_id).update(
            started=True
        )

    @classmethod
    def save_results(cls: type, match_id: int, results: dict) -> None:
        Match.objects.filter(pk=match_id).update(
            results=dumps(results)
        )
