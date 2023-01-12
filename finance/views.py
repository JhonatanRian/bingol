from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
import stripe
from bingoool.settings import STRIPE_TEST_SECRET_KEY
import json
from .models import Payment
# Create your views here.

stripe.api_key = STRIPE_TEST_SECRET_KEY


class CreatePaymentMethodView(View):

    def post(self, request, *args, **kwargs):

        try:
            data = json.loads(request.body)
            payment_method_type = 'card'
            params = {
                "amount": int(data.get("amount").replace(",", "").replace(".", "")),
                "currency": "brl",
                "payment_method_types": ["card"],
            }
        except:
            return HttpResponseBadRequest("request invalid")

        try:
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(**params)
            return HttpResponse(json.dumps({'payment_intent_id': intent.id}), content_type='application/json')
        except stripe.error.StripeError as e:
            return HttpResponseBadRequest(e)
        except Exception as e:
            return HttpResponseBadRequest(e)


class CreatePaymentMethod(View):
    def post(self, request, *args, **kwargs):
        ...


class PaymentDoneView(View):
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("merdaaaa")

    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body)
            payment_intent_id = payload.get("paymentIntentId")
            paymentMethodId = payload.get("paymentMethodId")
            amount = float(payload.get("amount").replace(".","").replace(",","."))
        except:
            return HttpResponseBadRequest("request invalid")

        # try:
        stripe.PaymentIntent.modify(payment_intent_id, payment_method=paymentMethodId)
        stripe.PaymentIntent.confirm(payment_intent_id)
            
        Payment.objects.create(
            payment_intent_id=payment_intent_id,
            payment_method_id=paymentMethodId,
            amount=amount,
            payer=request.user
        )
        return HttpResponse(json.dumps({"msg": "Pagamento concluido"}), content_type='application/json')
        # except Exception as e:
            # return HttpResponseBadRequest(e)