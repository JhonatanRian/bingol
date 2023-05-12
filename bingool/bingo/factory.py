from . import bingo
from .rules_awards import *

def globe(num_balls: int = 90):
	return bingo.Globe(max_length=num_balls)

def awards_default():
	awards = [
		Award(name='l1', rule= rule_linha1),
		Award(name='l2', rule= rule_linha2),
		Award(name='b', rule= rule_bingo, inactivate_card=True, amount_of_winners=3),
	]
	return awards

def match(awards: list[bingo.Award] = None):
	global globe
	if not awards:
		awards = awards_default()
	g = globe()
	return Match(awards, g)
