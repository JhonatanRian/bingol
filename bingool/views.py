from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import requests as rq
from bingoool.settings import API_GAME
import json


# Create your views here.

@method_decorator(login_required, name="dispatch")
class GameTemplateView(TemplateView):
    template_name = "main/game.html"

    def get_context_data(self, **kwargs):
        context = context = super(GameTemplateView, self).get_context_data(**kwargs)
        print(self.request.user.email)
        context['token'] = get_token(self.request.user.email)
        context['url_api'] = API_GAME
        
        return context

def get_token(email):
    response = rq.post(API_GAME+"/api/auth/token", json={"email": email})
    return json.loads(response.text)["access_token"]