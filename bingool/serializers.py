from rest_framework import serializers
from .models import Match, Card, Award, Winner, Bingo, Ball, CustomUser


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser

        fields = (
            "name",
            "money",
            "bonus"
        )


class VerySimpleUser(serializers.ModelSerializer):
    class Meta:
        model = CustomUser

        fields = (
            'name',
        )


class BallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ball

        fields = (
            'number',
            'drawn'
        )


class CardSerializer(serializers.ModelSerializer):
    
    balls = BallSerializer(many=True)
    
    class Meta:
        model = Card

        fields = (
            'balls',
        )


class WinnerSerializer(serializers.Serializer):
    user = VerySimpleUser()
    card = CardSerializer()

    class Meta:
        model = Winner
        fields = (
            'user',
            'card'
        )


class AwardSerializer(serializers.ModelSerializer):

    winners = serializers.SerializerMethodField()

    class Meta:
        model = Award

        fields = (
            'name',
            'value',
            'num_balls',
            'winners',
        )
    
    def get_winners(self, obj):
        winners = obj.winner.all()
        serializer = WinnerSerializer(winners, many=True)
        return serializer.data





class FirstMatchCurrentSerializer(serializers.Serializer):
    accumulate = serializers.SerializerMethodField()
    awards = serializers.SerializerMethodField()
    players = serializers.SerializerMethodField()
    display_wait = serializers.SerializerMethodField()

    def get_accumulate(self, obj):
        serializer = AwardSerializer(Award.objects.filter(initials="ac").last())
        return serializer.data

    def get_awards(self, obj):
        serializer = AwardSerializer(obj.award.all(), many=True)
        return serializer.data

    def get_players(self, obj):
        users_in_play = CustomUser.objects.filter(id__in=Card.objects.filter(bought=True, state__in=["inlive", "new"]))
        return users_in_play.count()

    def get_display_wait(self, obj):
        next_match = Match.objects.filter(finalized=False).order_by("datetime_to_start").first()
        return True if not obj.finalized and not next_match.started else False



class MatchCurrentSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    accumulate = serializers.SerializerMethodField(required=False)
    awards = serializers.SerializerMethodField()
    players = serializers.SerializerMethodField()
    display_wait = serializers.SerializerMethodField()
    datetime_initials = serializers.SerializerMethodField()

    def get_awards(self, obj):
        serializer = AwardSerializer(obj.award.all(), many=True)
        return serializer.data

    def get_players(self, obj):
        users_in_play = CustomUser.objects.filter(id__in=Card.objects.filter(bought=True, state__in=["inlive", "new"]))
        return users_in_play.count()

    def get_display_wait(self, obj):
        next_match = Match.objects.filter(finalized=False).order_by("datetime_to_start").first()
        return True if obj.finalized and not next_match.started else False

    def get_datetime_initials(self, obj):
        return obj.datetime_to_start
    
    def get_accumulate(self, obj):
        serializer = AwardSerializer(Award.objects.filter(initials="ac").last())
        return serializer.data


class NextMatchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    number_cards_allowed = serializers.IntegerField()
    unitary_value = serializers.SerializerMethodField()
    next_round_prize = serializers.SerializerMethodField()
    num_next_cards = serializers.SerializerMethodField()

    def get_unitary_value(self, obj):
        return obj.unitary_value_card

    def get_next_round_prize(self, obj):
        return obj.value_award_all

    def get_num_next_cards(self, obj):
        cards_count = Card.objects.filter(state="new", bought=True, user=self.context._request.user).count()
        return cards_count


class SyncSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    start_datetime = serializers.SerializerMethodField()
    started = serializers.BooleanField()
    finalized = serializers.BooleanField()
    standby = serializers.SerializerMethodField()

    def get_start_datetime(self, obj):
        return obj.datetime_to_start

    def get_standby(self, obj):
        bingo = Bingo.objects.filter(id=1).first()
        return bingo.standby


class AwardUser(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.DecimalField(decimal_places=2, max_digits=6)


class WinnerUserSerializer(serializers.Serializer):
    amount_received = serializers.DecimalField(max_digits=10, decimal_places=2)
    user = VerySimpleUser()
    card = CardSerializer()
    award = AwardUser()


class BingoSerializer(serializers.Serializer):
    ball_drawn = serializers.IntegerField()
    balls = serializers.SerializerMethodField()
    standby = serializers.BooleanField()
    color = serializers.CharField()
    finalized = serializers.SerializerMethodField()
    winners = serializers.SerializerMethodField()

    def get_finalized(self, obj):
        return self.context["match"].finalized

    def get_winners(self, obj):
        winners = Winner.objects.filter(award__match_id=self.context["match"].id)
        serializer = WinnerUserSerializer(winners, many=True)
        return serializer.data
    
    def get_balls(self, obj):
        balls = obj.ball.all()
        serializer = BallSerializer(balls, many=True)
        return serializer.data

