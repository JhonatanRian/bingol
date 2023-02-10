from .models import Match, Bingo, Card
from .serializers import MatchCurrentSerializer, FirstMatchCurrentSerializer,  NextMatchSerializer, SyncSerializer, BingoSerializer, CardSerializer, AuthSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .background_task import CreateCardsBackground


@api_view(['GET'])  
def match_current(request):
    match = Match.objects.filter(started=True).order_by('-datetime_to_start').first()

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
    match = Match.objects.filter(started=True).order_by('-datetime_to_start').first()
    bingo = Bingo.objects.filter(id=1).first()
    serializer = BingoSerializer(bingo, context={"match": match})
    return Response(serializer.data)

@api_view(["GET", "POST"])
def cards(request):
    if request.method == "POST":
        num_card = int(request.data.get("number_cards"))

        match = Match.objects.filter(started=False).order_by("datetime_to_start").first()
        cards = Card.objects.filter(bought=True, state="new", user=request.user)

        if not match:
            raise ParseError("Sem pré partida disponivel para calcular a compra")

        if (num_card + len(cards)) > match.number_cards_allowed:
            raise ParseError("Não é possivel comprar essa quantidade de cartelas")

        money = request.user.money
        bonus = request.user.bonus
        payable = num_card * match.unitary_value_card

        if payable > money+bonus:
            raise ParseError("Sem créditos suficientes")

        if (money > payable):
            money, bonus = money - payable, bonus
        else:
            money, bonus = 0, bonus - (payable - money)
        user = request.user

        user.money = money
        user.bonus = bonus
        user.save()

        cards_payable = []
        for card in range(num_card):
            cards_payable.append(Card(user=request.user, bought=True))

        Card.objects.bulk_create(cards_payable)

        CreateCardsBackground(request.user).start()

        return Response(data={"msg": "success"})
        
    match = Match.objects.filter(started=True).order_by('-datetime_to_start').first()
    cards = Card.objects.filter(match=match, user=request.user, state="inlive", bought=True)
    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def auth_me(request):
    serializer = AuthSerializer(request.user)
    return Response(serializer.data)