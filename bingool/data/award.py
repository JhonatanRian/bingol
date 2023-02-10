from bingool.models import Award

class RepositoryAward:

    @classmethod
    def get(cls: type, award_id: int) -> Award:
        return Award.objects.filter(id=award_id).first()

    @classmethod
    def get_accumulate(cls: type) -> Award:
        return Award.objects.filter(initials="ac").order_by("-datetime_created").first()