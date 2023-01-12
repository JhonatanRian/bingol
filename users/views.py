from django.shortcuts import render

from django.views.generic.base import TemplateView
from finance.forms import PaymentMethodsModelForm
from bingoool.settings import STRIPE_TEST_PUBLISHABLE_KEY
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bingool.models import Match

# Create your views here.

@method_decorator(login_required, name="dispatch")
class PainelUsersView(TemplateView):
    template_name = "main/painel.html"

    def get_context_data(self, **kwargs):
        context = context = super(PainelUsersView, self).get_context_data(**kwargs)
        form = PaymentMethodsModelForm()

        context["PUBLISHABLE_KEY"] = STRIPE_TEST_PUBLISHABLE_KEY
        context['form'] = form
        context['user'] = self.request.user
        context['match_current'] = Match.objects.filter(started=True)
        context['payments'] = self.request.user.payment.all().order_by('-datetime_saved')[:30]

        return context

    def post(self, request, *args, **kwargs):
        form = PaymentMethodsModelForm(request.POST)

