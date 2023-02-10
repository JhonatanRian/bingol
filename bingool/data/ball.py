from bingool.models import Ball, Bingo
from typing import List

class RepositoryBall:
	
	@classmethod
	def create_balls(cls: type, bingo_model: Bingo) -> List[Ball]:
		"""Cria as bolas para sorteio. São criadas com os numeros de 1 a 90.

		Args:
			cls (type): classe chamada.
			bingo_model (models.Bingo): Um modelo que será usado para linkar as bolas atravez do id.

		Returns:
			List[models.Ball]: lista de modelos models.Ball
		"""

		for num in range(1, 91):
			Ball.objects.create(
				number=num,
				drawn=False,
				bingo_id=bingo_model.id
				)

	@classmethod
	def all(cls: type) -> List[Ball]:
		return Ball.objects.all()

	@classmethod
	def draw_true(cls: type, number: int) -> None:
		ball_model = Ball.objects.get(number=number)
		ball_model.drawn = True
		ball_model.save()

	@classmethod
	def drawn_false(cls: type, number: int) -> None:
		ball_model = Ball.objects.get(number=number)
		ball_model.drawn = False
		ball_model.save()

	@classmethod
	def delete(cls: type, ball_id: int) -> None:
		ball_model = Ball.objects.get(pk=ball_id)
		ball_model.delete()

	@classmethod
	def get(cls: type, number: int) -> Ball:
		return Ball.objects.filter(number=number).first()

	@classmethod
	def reset(cls: type) -> None:
		Ball.objects.filter(drawn=True).update(drawn=False)