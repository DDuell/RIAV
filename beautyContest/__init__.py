from otree.api import *
import random
from decimal import Decimal
import numpy as np

#******************************************************************************#
# Constants
#******************************************************************************#
class Constants(BaseConstants):
    name_in_url = 'beautyContest1'
    players_per_group = None
    num_rounds = 1 
    prize = 10

#******************************************************************************#
# Subsession
#******************************************************************************#
class Subsession(BaseSubsession): 
    pass
  
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
  groupID = models.CharField()
  playerInSession = models.IntegerField()
  beautyContest_payoffs = models.IntegerField(initial = 0)
  choice = models.FloatField()
  choiceDone = models.IntegerField(initial=99)
  otherChoice1 = models.FloatField()
  otherChoice2 = models.FloatField()
  otherChoice3 = models.FloatField()
  average = models.FloatField() 
  twoThirdsAverage = models.FloatField() 
  closestGuess = models.FloatField()
  
#******************************************************************************#
# Pages
#******************************************************************************#
# Beauty contest introduction
#*****************************************************************************#
class BeautyContestIntroduction(Page):
    @staticmethod
    def vars_for_template(player: Player):
      player.treatment = player.participant.treatment
      player.numStage = player.participant.numStage
      
#*****************************************************************************#
# Choice
#*****************************************************************************#
class Choice(Page):
    form_model = 'player'
    form_fields = ['choice']

#*****************************************************************************#
# Results
#*****************************************************************************#
class Results(Page):
    @staticmethod 
    def vars_for_template(player: Player):
      players = player.subsession.get_players()
      playersDone = [p for p in players if p.choiceDone!=99]
      if len(playersDone)>2:
        player.otherChoice1 = playersDone[-1].choice
        player.otherChoice2 = playersDone[-2].choice
        player.otherChoice3 = playersDone[-3].choice
      elif len(playersDone)==2:
        player.otherChoice1 = playersDone[-1].choice
        player.otherChoice2 = playersDone[-2].choice
        player.otherChoice3 = player.participant.beautyOtherChoice3
      elif len(playersDone)==1:
        player.otherChoice1 = playersDone[-1].choice
        player.otherChoice2 = player.participant.beautyOtherChoice2
        player.otherChoice3 = player.participant.beautyOtherChoice3
      else:
        player.otherChoice1 = player.participant.beautyOtherChoice1
        player.otherChoice2 = player.participant.beautyOtherChoice2
        player.otherChoice3 = player.participant.beautyOtherChoice3

      player.otherChoice1 = round(player.otherChoice1)
      player.otherChoice2 = round(player.otherChoice2)
      player.otherChoice3 = round(player.otherChoice3)
      player.choice = round(player.choice)
      
      player.average = (player.choice + player.otherChoice1 + 
        player.otherChoice2 + player.otherChoice3)/4
      player.twoThirdsAverage = round((2/3)*player.average)
      if(
        abs(player.choice-player.twoThirdsAverage)<
        abs(player.otherChoice1-player.twoThirdsAverage) and
        abs(player.choice-player.twoThirdsAverage)<
        abs(player.otherChoice2-player.twoThirdsAverage) and
        abs(player.choice-player.twoThirdsAverage)<
        abs(player.otherChoice3-player.twoThirdsAverage)):
          player.closestGuess = 1
          player.beautyContest_payoffs = Constants.prize
      else: 
        player.closestGuess = 0
        player.beautyContest_payoffs = 0
      player.participant.beautyContest_payoffs = player.beautyContest_payoffs

      return {
            'nextStage': player.numStage + 1 
        }

    @staticmethod
    def before_next_page(player: Player,timeout_happened):
      player.participant.numStage = player.participant.numStage + 1
               
#*****************************************************************************#
                             
page_sequence = [
    BeautyContestIntroduction,
    Choice,
    Results
]
