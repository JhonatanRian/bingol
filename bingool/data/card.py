from typing import List
from bingool.models import Card

class RepositoryCard():

    @classmethod
    def get(cls: type, card_id: int) -> Card:
        return Card.objects.filter(pk=card_id).first()

    @classmethod
    def get_all_new_cards(cls: type) -> List[Card]:
        return Card.objects.filter(state="new", bought=True)

    @classmethod
    def update_inlive_all_new_cards(cls: type, match_id: int) -> None:
        Card.objects.filter(state="new", bought=True).update(
            state="inlive",
            match_id=match_id
        )

    @classmethod
    def update_finalized_all_cards(cls: type, match_id: int) -> None:
        Card.objects.filter(state="inlive", match_id=match_id).update(
            state="finalized"
        )

    @classmethod
    def update_inlive_cards(cls: type, cards: list[Card], match_id: int) -> None:
        Card.objects.filter(state="new", bought=True).update(
            state="inlive",
            match_id=match_id
        )
