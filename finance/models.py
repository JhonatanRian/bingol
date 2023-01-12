from django.db import models
from users.models import CustomUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
# Create your models here.


class PaymentMethod(models.Model):
    METHODS_PAYMENT_CHOICES = [
        ("card", "Cartão")
    ]
    method_type_name = models.CharField(
        "Método de pagamento", max_length=30, choices=METHODS_PAYMENT_CHOICES)
    datetime_created = models.DateTimeField(
        "Data de criação ", auto_now_add=True)
    id_stripe = models.CharField("id stripe", max_length=300)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class CardPayment(PaymentMethod):
    number = models.IntegerField("Número do cartão")
    exp_date = models.DateField("Data de Expiração", blank=False)
    cvc = models.IntegerField("CVC", blank=False,)

    class Meta:
        db_table = "card_payment"
        verbose_name = "Cartão"
        verbose_name_plural = "Cartões"


class Payment(models.Model):
    datetime_saved = models.DateTimeField(auto_now_add=True)
    date_saved = models.DateField("Data do pagamento", auto_now_add=True)
    payment_intent_id = models.CharField(
        "Id payment intent stripe", max_length=255)
    amount = models.DecimalField(
        "Valor da compra", decimal_places=2, max_digits=7)
    payment_method_id = models.CharField(
        "Id do metódo de pagamento", max_length=255)
    payer = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name="payment")

    class Meta:
        db_table = "payment"
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
        # ordering = ['datetime_saved']


# class Boleto(PaymentMethod):
#     cpf_cnpj = models.IntegerField("CPF/CNPJ", blank=False)
#     name = models.CharField("Nome", max_length=255)
#     country = models.CharField("País", max_length=255)
#     adress = models.ForeignKey("Adress", on_delete=models.CASCADE)

#     class Meta:
#         db_table = "boleto"
#         verbose_name = "Boleto"
#         verbose_name_plural = "Boletos"


# class Adress(models.Model):
#     adress_1 = models.CharField("Endereço 1", max_length=555)
#     adress_2 = models.CharField("Endereço 1", max_length=555)
#     city = models.CharField("Cidade", max_length=255)
#     state = models.CharField("Estado", max_length=155)
#     postal_code = models.IntegerField("Código postal")

#     class Meta:
#         db_table = "adress"
#         verbose_name = "Endereço"
#         verbose_name_plural = "Endereços"


@receiver(post_save, sender=Payment)
def user_payment_post_save(sender, instance, **kwargs):
    user: CustomUser = CustomUser.objects.get(id=instance.payer.id)
    user.money = float(instance.amount) + float(user.money)
    user.save()
    send_mail(
        'Payment Confirmation',
        'Thank you for your payment!',
        'bingooolVip@bingol.vip',
        [instance.payer.email],
        fail_silently=False,
    )
