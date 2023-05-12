from .bingo import *

def rule_linha1(card: Card, award: Award):
	lines = [card.line1_win, card.line2_win, card.line3_win]
	num_line_true = len([value for value in lines if value])
	
	if num_line_true == 1:
		award.amount_of_winners = award.amount_of_winners - 1
		award.sub_prizes_obtained += 1
		return Winner(award=award, card=card)


def rule_linha2(card: Card, award: Award):
	lines = [card.line1_win, card.line2_win, card.line3_win]
	num_line_true = len([value for value in lines if value])

	if num_line_true == 2:
		award.amount_of_winners = award.amount_of_winners - 1
		award.sub_prizes_obtained += 1

		return Winner(award=award, card=card)


def rule_bingo(card: Card, award: Award):
	lines = [card.line1_win, card.line2_win, card.line3_win]
	num_line_true = len([value for value in lines if value])
	
	if num_line_true == 3:
		award.amount_of_winners = award.amount_of_winners - 1
		award.sub_prizes_obtained += 1

		if award.amount_of_winners >= 0:

			name_award = f"{award.name}{award.sub_prizes_obtained}"
			sub_award = Award(name=name_award, 
							rule=award.rule,
							inactivate_card=award.inactivate_card,
							amount_of_winners=1)
			return Winner(award=sub_award, card=card) if num_line_true == 3 else False

		return Winner(award=award, card=card)