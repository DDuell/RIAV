from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json, 
)

import csv
import itertools
import random
import math

from django import forms
from localflavor.us.models import USStateField
from decimal import Decimal

author = 'Your name here'

doc = """
Your app description
"""

class Constants(BaseConstants):
    name_in_url = 'riskGame'
    players_per_group = 2
    num_rounds = 1
    num_players = 2
    
    violet_player1_amount = black_player2_amount = c(300)
    violet_player1_amount = black_player2_amount = c(200)
    mismatch_amount = c(0)
    quiz_player1_correct = c(0)
    quiz_player2_correct = c(0)
    quiz_maximum_offered_points = c(300)

class Subsession(BaseSubsession): 
    def creating_session(self):
         self.group_randomly(fixed_id_in_group=True)
                                        
class Group(BaseGroup):
    pass

class Player(BasePlayer):   
    groupID = models.StringField() 
    
    def role(self):
        if self.subsession.round_number == 1:
            if self.id_in_group == 1:
                return 'Player 1'
            else: 
                return 'Player 2'
        else:
            if self.in_round(1).id_in_group == 1:
                return 'Player 1'
            elif self.in_round(1).id_in_group == 2:
                return 'Player 2'

    quiz_question_player1 = models.CurrencyField(min=0, max=Constants.quiz_maximum_offered_points)

    quiz_question_player2 = models.CurrencyField(min=0, max=Constants.quiz_maximum_offered_points)

    choice = models.CharField(
        choices=['Violet', 'Black'],
        doc="""Either violet or black""",
        widget=widgets.RadioSelect()
    )
    
    def is_training_question_player1_correct(self):
        return (self.training_question_1_player1 ==
                Constants.training_1_player1_correct)

    def is_training_question_black_correct(self):
        return (self.training_question_1_player2 ==
                Constants.training_1_player2_correct)

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]
        
        
        
        
        
        
        
        
        