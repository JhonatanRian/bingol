from bingool.models import Winner


class RepositoryWinner:

    @classmethod
    def create_winner(cls: type, user_id: int, award_id: int, card_id: int, amount_received: float) -> Winner:
        winner = Winner.objects.create(
            user_id=user_id,
            card_id=card_id,
            award_id=award_id,
            amount_received=amount_received
        )
        return winner

    @classmethod
    def get(cls: type, award_id: int, card_id: int) -> Winner:
        winner = Winner.objects.filter(award_id=award_id, card_id=card_id).first()
        return winner
        