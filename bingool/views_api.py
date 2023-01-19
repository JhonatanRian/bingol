from .models import Match, Bingo, Card, Ball
from .serializers import MatchCurrentSerializer, FirstMatchCurrentSerializer, NextMatchSerializer, SyncSerializer, BingoSerializer, CardSerializer, AuthSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from .utils import create_lines

@api_view(['GET'])  
def match_current(request):
    match = Match.objects.filter(started=True).order_by('datetime_to_start').first()

    if not match:
        match = Match.objects.filter(finalized=False).order_by("datetime_to_start").first()
        serializer = FirstMatchCurrentSerializer(match)
        return Response(serializer.data)
    serializer = MatchCurrentSerializer(match)
    return Response(serializer.data)

@api_view(['GET'])  
def next_match(request):
    match = Match.objects.filter(started=False).order_by("datetime_to_start").first()
    serializer = NextMatchSerializer(match, context=request)
    return Response(serializer.data)

@api_view(['GET'])
def sync(request):
    match = Match.objects.filter(finalized=False).order_by("datetime_to_start").first()
    serializer = SyncSerializer(match)
    return Response(serializer.data)

@api_view(["GET"])
def bingo(request):
    match = Match.objects.filter(started=True).order_by('datetime_to_start').first()
    bingo = Bingo.objects.filter(id=1).first()
    serializer = BingoSerializer(bingo, context={"match": match})
    return Response(serializer.data)

@api_view(["GET", "POST"])
def cards(request):
    if request.method == "POST":
        num_card = int(request.data.get("num_cards"))
        bingo = Bingo.objects.get(id=1)
        match = Match.objects.filter(started=False).order_by("datetime_to_start").first()
        cards = Card.objects.filter(bought=True, state="new", user=request.user)

        if (num_card + len(cards)) > match.number_cards_allowed:
            return APIException(detail="Numero de compra impossivel")

        money = request.user.money
        bonus = request.user.bonus
        payable = num_card * match.unitary_value_card

        if payable > money+bonus:
            return APIException(detail="sem créditos suficiente")

        if (money > payable):
            money, bonus = money - payable, bonus
        else:
            money, bonus = 0, bonus - (payable - money)
        user = request.user

        user.money = money
        user.bonus = bonus

        cards_payable = []
        for card in range(num_card):
            cards_payable.append(Card.objects.create(user=user))
        
        for card in cards_payable:
            lines = create_lines()
            numbers = lines[0] + lines[1] + lines[2]

            for number in numbers:
                card.balls.add(Ball.objects.get(number=number))

        return Response(data={"msg": "success"})
        
    match = Match.objects.filter(started=True).order_by('datetime_to_start').first()
    cards = Card.objects.filter(match=match, user=request.user, state="inlive", bought=True).order_by("id")
    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def auth_me(request):
    serializer = AuthSerializer(request.user)
    return Response(serializer.data)