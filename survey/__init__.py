from otree.api import *
import random
from decimal import Decimal
import numpy as np

#******************************************************************************#
# Constants
#******************************************************************************#
class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1 

#******************************************************************************#
# Subsession
#******************************************************************************#
class Subsession(BaseSubsession): 
    def creating_session(self):
        exchange_rate = c(self.session.config['real_world_currency_per_point']*100)
                                                 
#******************************************************************************#
# Group
#******************************************************************************#
class Group(BaseGroup):
    pass
                          
#******************************************************************************#
# Player
#******************************************************************************#
class Player(BasePlayer):
    treatment = models.CharField()
    numStage = models.IntegerField()
    q_age = models.PositiveIntegerField(verbose_name='What is your age?',
                                        choices=range(13, 125),
                                        initial=None)
    q_gender = models.CharField(initial=None,
                                choices=['Male', 'Female','Other'],
                                verbose_name='What is your gender?',
                                widget=widgets.RadioSelect())
    
    q_race = models.CharField(initial=None,
                                choices=['White non-Hispanic', 
                                'Black non-Hispanic','Hispanic','Other'],
                                widget=widgets.RadioSelect())

    q_education = models.CharField(initial=None,
                                choices=['High school diploma or equivalent',
                                'Some college but no degree',
                                'Associate degree or equivalent',
                                "Bachelor's degree",
                                'Graduate degree',
                                'Other'],
                                widget=widgets.RadioSelect())

    q_groupID = models.CharField(initial=None,
      choices=['Klees', 'Kandinskys','Chagalls','Picassos','No group assigned'],
      verbose_name='What was your group?',
      widget=widgets.RadioSelect())


    q_groupClose =  models.CharField(
        verbose_name='On a scale from 1 (not at all) to 10 (very much), how close did you feel to members of your own group',
        choices=['0','1','2','3','4','5','6','7','8','9','10','No group assigned'],
        widget=widgets.RadioSelectHorizontal())
    
    q_whatAbout = models.TextField(verbose_name='What do you think was this experimenter about?')
        
    q_choices = models.TextField(verbose_name='In stage 2 of the experiment, how did you make your choice between A and B?')
    
    q_clear = models.TextField(verbose_name='Where the instructions clear? If not, which part of the instructions was not clear?')
    gameEarnings = models.CurrencyField(initial = 0)
    totalEarnings = models.CurrencyField(initial = 0)
    finished = models.CharField()
    label = models.CharField()
  
#******************************************************************************#
# Pages
#*****************************************************************************#
# Survey questions
#*****************************************************************************#
class questions(Page):
  form_model = 'player'
  form_fields = ['q_age','q_gender','q_race','q_education','q_groupID',
    'q_groupClose','q_choices','q_whatAbout','q_clear']
  
  @staticmethod
  def vars_for_template(player: Player):
    player.treatment = player.participant.treatment
    player.numStage = player.participant.numStage
    
  @staticmethod
  def before_next_page(player: Player,timeout_happened):  
      exchange_rate = player.session.config['real_world_currency_per_point']
      participation_fee = player.session.config['participation_fee']
      if (player.treatment != 'noIdentity' and 
      player.treatment != 'noIdentityLowThreshold'):
        player.gameEarnings = cu((player.participant.painterQuiz_payoffs + 
          player.participant.riskGame_payoffs + 
          player.participant.publicGoodsGame_payoffs + 
          player.participant.beautyContest_payoffs +
          player.participant.bombGame_payoffs)*exchange_rate)
      else:
        player.gameEarnings = cu((player.participant.riskGame_payoffs + 
          player.participant.publicGoodsGame_payoffs + 
          player.participant.beautyContest_payoffs +
          player.participant.bombGame_payoffs)*exchange_rate)
      player.totalEarnings = cu(player.gameEarnings + participation_fee)
      player.payoff = player.gameEarnings
      player.participant.finished = True 
      player.finished = 'True'
      player.label = participant.label
      
#******************************************************************************#
# Final payoffs
#*****************************************************************************#
class finalPayoffs(Page):
    @staticmethod
    def vars_for_template(player: Player):
      participation_fee = player.session.config['participation_fee']
      return {
        'participation_fee':participation_fee
      }

page_sequence = [
    questions,
    finalPayoffs
]

