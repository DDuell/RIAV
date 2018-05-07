from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
import math
import time

class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1
                                                                           
class ChoicePlayer1(Page):
    form_model = models.Player
    form_fields = ['choicePlayer1']
    
    def is_displayed(self):
        players = self.subsession.get_players()
        for p in players:
            p.groupID = p.participant.vars['groupID']
        return self.player.id_in_group == 1 
    
    def vars_for_template(self):                                        
        return {
            'groupID': self.player.groupID,
            'groupID_other': self.player.other_player().groupID,
            'player1_left_up_payoffs': Constants.player1_left_up_payoffs[self.subsession.round_number], 
            'player1_left_down_payoffs': Constants.player1_left_down_payoffs[self.subsession.round_number], 
            'player1_right_up_payoffs': Constants.player1_right_up_payoffs[self.subsession.round_number], 
            'player1_right_down_payoffs': Constants.player1_right_down_payoffs[self.subsession.round_number],
            'player2_down_left_payoffs': Constants.player2_up_left_payoffs[self.subsession.round_number], 
            'player2_down_right_payoffs': Constants.player2_up_right_payoffs[self.subsession.round_number], 
            'player2_up_left_payoffs': Constants.player2_down_left_payoffs[self.subsession.round_number], 
            'player2_up_right_payoffs': Constants.player2_down_right_payoffs[self.subsession.round_number]
        }   
        
class ChoicePlayer2(Page):
    form_model = models.Player
    form_fields = ['choicePlayer2']

    def is_displayed(self):
        return self.player.id_in_group == 2 
    
    def vars_for_template(self):                                        
        return {
            'groupID': self.player.groupID,
            'groupID_other': self.player.other_player().groupID,
            'player1_left_up_payoffs': Constants.player1_left_up_payoffs[self.subsession.round_number], 
            'player1_left_down_payoffs': Constants.player1_left_down_payoffs[self.subsession.round_number], 
            'player1_right_up_payoffs': Constants.player1_right_up_payoffs[self.subsession.round_number], 
            'player1_right_down_payoffs': Constants.player1_right_down_payoffs[self.subsession.round_number],
            'player2_down_left_payoffs': Constants.player2_up_left_payoffs[self.subsession.round_number], 
            'player2_down_right_payoffs': Constants.player2_up_right_payoffs[self.subsession.round_number], 
            'player2_up_left_payoffs': Constants.player2_down_left_payoffs[self.subsession.round_number], 
            'player2_up_right_payoffs': Constants.player2_down_right_payoffs[self.subsession.round_number]
        }                

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()
        self.group.set_payoffs_display()

    def body_text(self):
        return "Waiting for the other participants to make their choice."
		
class Results(Page):
    def vars_for_template(self):
        return {
            'round_number': self.subsession.round_number,
            'player1_left_up_payoffs': Constants.player1_left_up_payoffs[self.subsession.round_number], 
            'player1_left_down_payoffs': Constants.player1_left_down_payoffs[self.subsession.round_number], 
            'player1_right_up_payoffs': Constants.player1_right_up_payoffs[self.subsession.round_number], 
            'player1_right_down_payoffs': Constants.player1_right_down_payoffs[self.subsession.round_number],
            'player2_down_left_payoffs': Constants.player2_up_left_payoffs[self.subsession.round_number], 
            'player2_down_right_payoffs': Constants.player2_up_right_payoffs[self.subsession.round_number], 
            'player2_up_left_payoffs': Constants.player2_down_left_payoffs[self.subsession.round_number], 
            'player2_up_right_payoffs': Constants.player2_down_right_payoffs[self.subsession.round_number]
        }
        
class ResultsRiskGame(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds
        
    def vars_for_template(self):
        final_payoff_risk_game = self.participant.payoff 
        players = self.subsession.get_players()
        for p in players:
            p.participant.vars['final_payoff_risk_game'] = p.participant.payoff 
        return {
            'final_payoffs_risk_game': final_payoff_risk_game
        }        

class riskElicitation1(Page):
    form_model = models.Player
    form_fields = ['riskElicitation_self']
    
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds
        
class riskElicitation2(Page):
    form_model = models.Player
    form_fields = ['riskElicitation_own','riskElicitation_other']
    
    def vars_for_template(self):
        players = self.subsession.get_players()
        for p in players:
            if p.groupID == 'Green':
                other_groupID = 'Blue'
            else:
                other_groupID = 'Green'
                
        return {
            'other_groupID': other_groupID
        }

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds
        
 
class ResultsRiskElicitationWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs_riskElicitation()

    def body_text(self):
        return "Waiting for the other participants to make their choic."
		
class ResultsRiskElicitation(Page):
    def vars_for_template(self):
        return {
            'round_number': self.subsession.round_number
        } 

class FinalPayoffs(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds
        
    def vars_for_template(self):
        return {
            'final_earnings': self.participant.payoff_plus_participation_fee()
        }  
                             
page_sequence = [
    Introduction,
    ChoicePlayer1,
    ChoicePlayer2,
    ResultsWaitPage,
    Results,
    ResultsRiskGame,
    riskElicitation1,
    riskElicitation2,
    FinalPayoffs    
]
