from django import forms
from .models import CardPayment

class PaymentMethodsModelForm(forms.ModelForm):

    class Meta:
        model = CardPayment
        fields = ("method_type_name", "number", "exp_date", "cvc")