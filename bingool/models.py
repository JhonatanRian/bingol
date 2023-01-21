from django.db import models
from users.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from decimal import Decimal
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from pytz import utc
# Create your models here.

datetime.now()

class Base(models.Model):
    datetime_created = models.DateTimeField(
        "Data de criação ", auto_now_add=True)

    class Meta:
        abstract = True


class Match(Base):
    datetime_to_start = models.DateTimeField(
        "Data e o Horario a ser iniciado", blank=False)
    date_to_start = models.DateField("Data a ser iniciada", blank=False, help_text="Horario não deve ser no passado, escolha um tempo com 10 minutos depois da ultima partida marcada")
    started = models.BooleanField("iniciou", default=False)
    finalized = models.BooleanField("finalizou", default=False)
    automatic = models.BooleanField("Sorteio automatico", default=False, )
    unitary_value_card = models.DecimalField(
        "Unidade da cartela", max_digits=4, decimal_places=2, blank=False)
    number_cards_allowed = models.IntegerField(
        "Numero de cartelas permitida por usuario", blank=False)
    value_award_all = models.DecimalField(
        "Valor total do prêmio", max_digits=6, decimal_places=2, blank=False)
    results = models.JSONField("dados da partida", blank=True, null=True)

    def clean(self):
        if self.datetime_to_start < datetime.now(utc):
            raise ValidationError("A partida deve ter como horario para iniciar no futuro e não no passado")

        if Match.objects.exists():
            last_match = Match.objects.all().order_by("datetime_to_start").last()

            if self.datetime_to_start < (last_match.datetime_to_start + timedelta(minutes=11)):
                if matchs := Match.objects.filter(datetime_to_start__range=(self.datetime_to_start - timedelta(minutes=9, seconds=59), self.datetime_to_start + timedelta(minutes=9, seconds=59))):
                    if (matchs.count() < 2) and matchs.contains(self):
                        return
                    raise ValidationError(f"O horario da partida é invalido por que existe partida salva onde esse horario se encaixa dentro do limite de tempo de jogo.")
                elif self.datetime_created != None:
                    return
                
                raise ValidationError(f"Uma partida precisa de no minimo 10 minutos para o bingo começar e finalizar, escolha uma data maior que {last_match.datetime_to_start - timedelta(hours=3)}, você só pode criar partidas depois desta data.")

            if self.datetime_to_start < last_match.datetime_to_start:
                
                raise ValidationError(f"A ultima partida criada ficou para iniciar em {last_match.datetime_to_start - timedelta(hours=3)}, você só pode criar partidas depois desta data.")



    class Meta:
        verbose_name = "Partida"
        verbose_name_plural = "Partidas"
        db_table = "match"

    def __str__(self) -> str:
        return f"id: {self.id}, finalized: {self.finalized}"


class Bot(Base):
    running = models.BooleanField("Sorteio altomático", default=False)

    class Meta:
        verbose_name = "Bot"
        db_table = "bot"


class Award(Base):
    OPTIONS_INITIALS = [
        ('l1', 'Linha 1'),
        ('l3', 'Linha 2'),
        ('b1', 'Bingo'),
        ('b2', 'Bingo2'),
        ('b3', 'Bingo3'),
        ('ac', 'Acummulado'),
    ]

    name = models.CharField("Nome", max_length=50,)
    value = models.DecimalField(
        "Valor", max_digits=6, decimal_places=2, blank=False)
    initials = models.CharField(
        "Iniciais", choices=OPTIONS_INITIALS, max_length=50)
    num_balls = models.IntegerField(
        "Numero de bolas para conseguir este prêmio", blank=False)
    match = models.ForeignKey(
        "Match", null=True, blank=False, on_delete=models.CASCADE, related_name="award")

    class Meta:
        verbose_name = "Prêmio"
        verbose_name_plural = "Prêmios"
        db_table = "award"

    def __str__(self) -> str:
        return self.name


class Winner(Base):
    amount_received = models.DecimalField(
        "Valor a receber", max_digits=10, decimal_places=2, blank=False, null=True)
    user = models.ForeignKey(CustomUser, null=False,
                             blank=False, on_delete=models.PROTECT)
    card = models.ForeignKey(
        'Card', null=False, blank=False, on_delete=models.PROTECT)
    award = models.ForeignKey(
        'Award', null=False, blank=False, on_delete=models.CASCADE, related_name="winner")

    class Meta:
        verbose_name = "Vencedor"
        verbose_name_plural = "Vencedores"
        db_table = "winner"

    def __str__(self) -> str:
        return self.user


class Bingo(Base):
    colors = [
        ("color1", "color1"), 
        ("color2", "color2"), 
        ("color3", "color3"), 
        ("color4", "color4"), 
        ("color5", "color5"), 
        ("color6", "color6"), 
        ("color7", "color7"), 
        ("color8", "color8"), 
        ("color9", "color9")]

    ball_drawn = models.IntegerField("Bola sorteada", null=True)
    standby = models.BooleanField("Bingo em espera", default=False)
    color = models.CharField(max_length=6, choices=colors, null=True)

    class Meta:
        verbose_name = "Bingo"
        verbose_name_plural = "Bingos"
        db_table = "bingo"


class Ball(Base):
    number = models.IntegerField("Bola", blank=False, null=False, unique=True)
    drawn = models.BooleanField("Sorteado", default=False)

    bingo = models.ForeignKey(
        "Bingo", null=False, blank=False, on_delete=models.CASCADE, related_name="ball")

    class Meta:
        verbose_name = "Bola"
        verbose_name_plural = "Bolas"
        db_table = "ball"


class Card(Base):
    OPTIONS_STATE = [
        ('new', 'Nova'),
        ('inlive', 'Em jogo'),
        ('finalized', 'Fora de jogo'),
    ]

    balls = models.ManyToManyField(
        "Ball", verbose_name="Bolas", through="BallsCards")
    state = models.CharField(
        "Estado da cartela", max_length=10, choices=OPTIONS_STATE, default='new')
    bought = models.BooleanField("Comprado", default=False)

    match = models.ForeignKey(Match, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=True,
                             blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Cartela"
        verbose_name_plural = "Cartelas"
        db_table = "card"


class BallsCards(Base):
    card = models.ForeignKey("Card", null=True, on_delete=models.CASCADE)
    ball = models.ForeignKey("Ball", null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "balls_cards"
        ordering = None

def create_accumulate():
    if not Award.objects.filter(initials="ac").exists():
        Award.objects.create(
            name="Accumulate",
            value=100,
            initials="ac",
            num_balls="28"
        )

@receiver(post_save, sender=Match)
def match_post_save(sender, instance: Match, **kwargs):
    awards_list = (
        ("linha 1", instance.value_award_all * Decimal(0.10), "l1", 5),
        ("linha 2", instance.value_award_all * Decimal(0.10), "l2", 10),
        ("Bingo", instance.value_award_all * Decimal(0.40), "b1", 15),
        ("Bingo 2", instance.value_award_all * Decimal(0.20), "b2", 15),
        ("Bingo 3", instance.value_award_all * Decimal(0.20), "b3", 15),
    )
    if not Award.objects.filter(match=instance).exists():
        for award in awards_list:
            Award.objects.create(
                name=award[0],
                value=award[1],
                initials=award[2],
                num_balls=award[3],
                match_id=instance.id
            )
    create_accumulate()
