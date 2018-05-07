from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
import math
import time
                
class Introduction(Page):
    timeout_seconds = 300
    
    def is_displayed(self):
        return self.subsession.round_number == 1
    
    def vars_for_template(self):        
        for p in self.subsession.get_players():
            if p.participant.vars['groupID'] == 'A':
                self.player.groupID = 'A'
            elif p.participant.vars['groupID'] == 'B':
                self.player.groupID = 'B'
                                
        return {
            'groupID': self.player.groupID
        }
							
class Quiz(Page):
    template_name = 'riskGame/Quiz.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['quiz_question_player1','quiz_question_player2']

    def vars_for_template(self):
        return {'num_q': 1}

class QuizFeedback(Page):
    template_name = 'riskGame/QuizFeedback.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 1,
               }
 
class ChoiceWaitPage(WaitPage):
    template_name = 'riskGame/ChoiceWaitpage.html'
     
    def after_all_players_arrive(self):
        return True
                                             
class Choice(Page):
    form_model = models.Player
    form_fields = ['choice']
    
    def vars_for_template(self):        
        for p in self.subsession.get_players():
            if p.participant.vars['groupID'] == 'A':
                self.player.groupID = 'A'
            elif p.participant.vars['groupID'] == 'B':
                self.player.groupID = 'B'
                                
        return {
            'groupID': self.player.groupID,
            'groupID_other': self.player.other_player().in_all_rounds()[0].groupID
            
        }        
            
page_sequence = [
    Introduction,
    Quiz,
    QuizFeedback,
    ChoiceWaitPage,
    Choice
]
