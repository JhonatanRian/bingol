import threading
from .models import *
from users.models import CustomUser
from .utils import create_lines

class CreateCardsBackground(threading.Thread):

    def __init__(self, user: CustomUser):
        self.user = user
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        try:
            cards_models = Card.objects.filter(user=self.user, implemented_lines=False)
            for card in cards_models:
                lines = create_lines()
                balls_models = Ball.objects.all()

                for i in range(1,4):
                    line_model = Line.objects.create(name=f"l{i}", card=card)
                    line = lines[i-1]
                    line_model.balls.add(*[balls_models.filter(number=ball).first() for ball in line])
                card.implemented_lines = True
                card.save()
        except Exception as err:
            print(err)
