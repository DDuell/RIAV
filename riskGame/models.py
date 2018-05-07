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
    
    player1_left_up_payoffs = [0,300,200,100,400]
    player1_left_down_payoffs = [0,150,300,200,500]
    player1_right_up_payoffs = [0,300,200,100,400]
    player1_right_down_payoffs = [0,100,250,300,500]
    player2_up_left_payoffs = [0,400,250,150,450]
    player2_up_right_payoffs = [0,300,200,100,400]
    player2_down_left_payoffs = [0,300,200,100,400]
    player2_down_right_payoffs = [0,300,200,100,400]

class Subsession(BaseSubsession): 
    def creating_session(self):
        self.group_randomly()
        
        exchange_rate = c(self.session.config['real_world_currency_per_point']*100)
        
        if self.round_number == 1:
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
            print("paying_round",paying_round)
                                        
class Group(BaseGroup):
    def set_payoffs(self):
        player1 = self.get_player_by_role('Player 1')
        player2 = self.get_player_by_role('Player 2')
        
        if self.subsession.round_number == self.session.vars['paying_round']:
            if player1.choicePlayer1 == 'Left' and player2.choicePlayer2 == 'Up': 
                player1.payoff = Constants.player1_left_up_payoffs[self.subsession.round_number]
                player2.payoff = Constants.player2_up_left_payoffs[self.subsession.round_number]           
            
            elif player1.choicePlayer1 == 'Left' and player2.choicePlayer2 == 'Down':
                player1.payoff = Constants.player1_left_down_payoffs[self.subsession.round_number]
                player2.payoff = Constants.player2_down_left_payoffs[self.subsession.round_number]
            
            elif player1.choicePlayer1 == 'Right' and player2.choicePlayer2 == 'Up':
                player1.payoff = Constants.player1_right_up_payoffs[self.subsession.round_number]
                player2.payoff = Constants.player2_up_right_payoffs[self.subsession.round_number]
                
            elif player1.choicePlayer1 == 'Right' and player2.choicePlayer2 == 'Down':
                player1.payoff = Constants.player1_right_down_payoffs[self.subsession.round_number]
                player2.payoff = Constants.player2_down_right_payoffs[self.subsession.round_number]
            
        else:
            player1.payoff = c(0)
            player2.payoff = c(0)
        
    def set_payoffs_display(self):
        player1 = self.get_player_by_role('Player 1')
        player2 = self.get_player_by_role('Player 2')
    
        if player1.choicePlayer1 == 'Left' and player2.choicePlayer2 == 'Up': 
            player1.payoff_display = Constants.player1_left_up_payoffs[self.subsession.round_number]
            player2.payoff_display = Constants.player2_up_left_payoffs[self.subsession.round_number]           
        
        elif player1.choicePlayer1 == 'Left' and player2.choicePlayer2 == 'Down':
            player1.payoff_display = Constants.player1_left_down_payoffs[self.subsession.round_number]
            player2.payoff_display = Constants.player2_down_left_payoffs[self.subsession.round_number]
        
        elif player1.choicePlayer1 == 'Right' and player2.choicePlayer2 == 'Up':
            player1.payoff_display = Constants.player1_right_up_payoffs[self.subsession.round_number]
            player2.payoff_display = Constants.player2_up_right_payoffs[self.subsession.round_number]
            
        elif player1.choicePlayer1 == 'Right' and player2.choicePlayer2 == 'Down':
            player1.payoff_display = Constants.player1_right_down_payoffs[self.subsession.round_number]
            player2.payoff_display = Constants.player2_down_right_payoffs[self.subsession.round_number]
                  
class Player(BasePlayer):   
    groupID = models.CharField()
    payoff_display = models.FloatField()
    
    def role(self):
        if self.id_in_group == 1:
            return 'Player 1'
        else: 
            return 'Player 2'

    choicePlayer1 = models.CharField(
        choices=['Left', 'Right'],
        widget=widgets.RadioSelect()
    )    
    
    choicePlayer2 = models.CharField(
        choices=['Up', 'Down'],
        widget=widgets.RadioSelect()    
    )
    
    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]
        
    riskElicitation_self = models.IntegerField(min=1, max=100)

    riskElicitation_own = models.IntegerField(min=1, max=100)
        
    riskElicitation_other = models.IntegerField(min=1, max=100)      
        
        
        
        
        
        
        