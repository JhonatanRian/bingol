from django.urls import path
from .views import CreatePaymentMethodView, PaymentDoneView

urlpatterns = [
    path('payment/create-payment-intent', CreatePaymentMethodView.as_view(), name="create_payment"),
    path('payment/done', PaymentDoneView.as_view(), name="payment_done"),
]
