from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from bingoool.settings import API_GAME
from rest_framework.authtoken.models import Token


# Create your views here.

@method_decorator(login_required, name="dispatch")
class GameTemplateView(TemplateView):
    template_name = "main/game.html"

    def get_context_data(self, **kwargs):
        context = context = super(GameTemplateView, self).get_context_data(**kwargs)
        context['token'] = Token.objects.get(self.request.user)
        context['url_api'] = API_GAME
        
        return context
