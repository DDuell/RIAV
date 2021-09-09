from otree.api import *
import random
from decimal import Decimal
import numpy as np

#******************************************************************************#
# Constants
#******************************************************************************#
class Constants(BaseConstants):
    name_in_url = 'publicGoodsGame1'
    players_per_group = None
    num_rounds = 1 
    endowment = 10
    multiplier = 2
    quizQuestion_correct = 5

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
  orderOfApps = models.IntegerField()
  groupID = models.CharField()
  numStage = models.IntegerField()
  choiceDone = models.IntegerField(initial=99)
  otherGroupID1 = models.CharField()
  otherGroupID2 = models.CharField()
  otherGroupID3 = models.CharField()
  quizQuestion = models.IntegerField()
  choice = models.IntegerField(
        min=0,
        max=Constants.endowment
    )
  otherChoice1 = models.IntegerField()
  otherChoice2 = models.IntegerField()
  otherChoice3 = models.IntegerField()
  PGOtherChoice1 = models.IntegerField()
  PGOtherChoice2 = models.IntegerField()
  PGOtherChoice3 = models.IntegerField()
  sumChoices = models.IntegerField()
  share = models.FloatField()
  publicGoodsGame_payoffs = models.FloatField(initial = 0)
  
#******************************************************************************#
# Pages
#******************************************************************************#
# Public goods game introduction
#*****************************************************************************#
class PublicGoodsGameIntroduction(Page):
    @staticmethod
    def is_displayed(player: Player):
      player.orderOfApps = player.participant.orderOfApps
      return player.orderOfApps==1
    
    @staticmethod
    def vars_for_template(player: Player):
      player.treatment = player.participant.treatment
      player.numStage = player.participant.numStage
      
      if (player.treatment != 'noIdentity' and
          player.treatment != 'noIdentityLowThreshold'):
        player.groupID = player.participant.groupID    
        player.otherGroupID1 = player.participant.otherGroupID1
        player.otherGroupID2 = player.participant.otherGroupID2
        player.otherGroupID3 = player.participant.otherGroupID3
        player.PGOtherChoice1 = player.participant.PGOtherChoice1
        player.PGOtherChoice2 = player.participant.PGOtherChoice2
        player.PGOtherChoice3 = player.participant.PGOtherChoice3
 
#*****************************************************************************#
# Quiz
#*****************************************************************************#
class Quiz(Page):
    form_model = 'player'
    form_fields = ['quizQuestion']
    
    @staticmethod
    def is_displayed(player: Player):
      return player.orderOfApps==1 
               
#*****************************************************************************#
# Quiz feedback
#*****************************************************************************#
class QuizFeedback(Page):
    @staticmethod
    def is_displayed(player: Player):
      return player.orderOfApps==1 
    
#*****************************************************************************#
# Choice
#*****************************************************************************#
class Choice(Page):
    form_model = 'player'
    form_fields = ['choice']
    
    @staticmethod
    def is_displayed(player: Player):
      return player.orderOfApps==1

#*****************************************************************************#
# Results
#*****************************************************************************#
class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
      return player.orderOfApps==1
    
    @staticmethod 
    def vars_for_template(player: Player):
      players = player.subsession.get_players()
      playersDone = [p for p in players if p.choiceDone!=99]
      if (player.participant.treatment!='noIdentity' and 
        player.participant.treatment!='noIdentityLowThreshold'):
          klees = [p for p in playersDone if p.groupID == 'Klee']
          kandinskys = [p for p in playersDone if p.groupID == 'Kandinsky']
          chagalls = [p for p in playersDone if p.groupID == 'Chagall']
          picassos = [p for p in playersDone if p.groupID == 'Picasso']
      
      # No identity treatment
      mu = Constants.endowment/2
      sigma = Constants.endowment/10
      if (player.participant.treatment=='noIdentity' or 
        player.participant.treatment=='noIdentityLowThreshold'):
          if len(playersDone)>2:
            player.otherChoice1 = playersDone[-1].choice
            player.otherChoice2 = playersDone[-2].choice
            player.otherChoice3 = playersDone[-3].choice
          elif len(playersDone)==2:
            player.otherChoice1 = playersDone[-1].choice
            player.otherChoice2 = playersDone[-2].choice
            player.otherChoice3 = player.participant.PGOtherChoice3
          elif len(playersDone)==1:
            player.otherChoice1 = playersDone[-1].choice
            player.otherChoice2 = player.participant.PGOtherChoice2
            player.otherChoice3 = player.participant.PGOtherChoice3
          else:
            player.otherChoice1 = player.participant.PGOtherChoice1
            player.otherChoice2 = player.participant.PGOtherChoice2
            player.otherChoice3 = player.participant.PGOtherChoice3
      
      else:  
        # Identity treatments
        if (player.otherGroupID1=="Klee"):
          if (len(klees)>0):
            player.otherChoice1 = klees[-1].choice
          else:
            player.otherChoice1 = player.participant.PGOtherChoice1
        elif (player.otherGroupID1=="Kandinsky"):
          if (len(kandinskys)>0):
            player.otherChoice1 = kandinskys[-1].choice
          else:
            player.otherChoice1 = player.participant.PGOtherChoice1 
        elif (player.otherGroupID1=="Chagall"):
          if (len(chagalls)>0):
            player.otherChoice1 = chagalls[-1].choice
          else:
            player.otherChoice1 = player.participant.PGOtherChoice1  
        elif (player.otherGroupID1=="Picasso"):
          if (len(picassos)>0):
            player.otherChoice1 = picassos[-1].choice
          else:
            player.otherChoice1 = player.participant.PGOtherChoice1 

        if (player.otherGroupID2=="Klee"):
          if (len(klees)>1):
            player.otherChoice2 = klees[-1].choice
          else:
            player.otherChoice2 = player.participant.PGOtherChoice2
        elif (player.otherGroupID2=="Kandinsky"):
          if (len(kandinskys)>1):
            player.otherChoice2 = kandinskys[-1].choice
          else:
            player.otherChoice2 = player.participant.PGOtherChoice2  
        elif (player.otherGroupID2=="Chagall"):
          if (len(chagalls)>0):
            player.otherChoice2 = chagalls[-1].choice
          else:
            player.otherChoice2 = player.participant.PGOtherChoice2  
        elif (player.otherGroupID2=="Picasso"):
          if (len(picassos)>0):
            player.otherChoice2 = picassos[-1].choice
          else:
            player.otherChoice2 = player.participant.PGOtherChoice2
 
        if (player.otherGroupID3=="Klee"):
          if (len(klees)>1):
            player.otherChoice3 = klees[-1].choice
          else:
            player.otherChoice3 = player.participant.PGOtherChoice3
        elif (player.otherGroupID3=="Kandinsky"):
          if (len(kandinskys)>1):
            player.otherChoice3 = kandinskys[-1].choice
          else:
            player.otherChoice3 = player.participant.PGOtherChoice3  
        elif (player.otherGroupID3=="Chagall"):
          if (len(chagalls)>0):
            player.otherChoice3 = chagalls[-1].choice
          else:
            player.otherChoice3 = player.participant.PGOtherChoice3  
        elif (player.otherGroupID3=="Picasso"):
          if (len(picassos)>0):
            player.otherChoice3 = picassos[-1].choice
          else:
            player.otherChoice3 = player.participant.PGOtherChoice3
      
      player.sumChoices = player.choice + player.otherChoice1 + player.otherChoice2 + player.otherChoice3
      player.share = (player.sumChoices*Constants.multiplier)/4
      player.publicGoodsGame_payoffs = Constants.endowment - player.choice + player.share 
      player.participant.publicGoodsGame_payoffs = player.publicGoodsGame_payoffs

      return {
            'nextStage': player.numStage + 1 
        }
        
    @staticmethod
    def before_next_page(player: Player,timeout_happened):
      player.participant.numStage = player.participant.numStage + 1
 
#*****************************************************************************#
                             
page_sequence = [
    PublicGoodsGameIntroduction,
    Quiz,
    QuizFeedback,
    Choice,
    Results
]
