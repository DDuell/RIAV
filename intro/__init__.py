from otree.api import *
import random
import json
import csv
import numpy as np

#******************************************************************************#
# Constants
#******************************************************************************#
class Constants(BaseConstants):
    name_in_url = 'introduction'
    players_per_group = None
    num_rounds = 1  
    endowment = 10
    multiplier = 2
    numPlayersConsidered = 20
    
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
    treatment = models.StringField(initial='Not assigned yet')
    groupID = models.CharField(initial='Not assigned yet')
    otherGroupID1 = models.CharField()
    otherGroupID2 = models.CharField()
    otherGroupID3 = models.CharField()
    orderOfApps = models.IntegerField()
    playerInSession = models.IntegerField()
      
#******************************************************************************#
# Pages
#******************************************************************************#
class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']

class experimentIntroduction(Page):
  @staticmethod
  def vars_for_template(player: Player):
    player.treatment=random.choice(['noIdentity','identity',
      'noIdentityLowThreshold','identityLowThreshold','identity4Groups',
      'identity4GroupsLowThreshold'])
    player.participant.treatment = player.treatment
    player.orderOfApps = random.randint(1,2)
    player.participant.orderOfApps = player.orderOfApps
    player.participant.numStage = 0
    if (player.treatment == 'identity' or 
      player.treatment == 'identityLowThreshold'):
          player.otherGroupID1 = random.choice(['Klee','Kandinsky'])
          player.otherGroupID2 = random.choice(['Klee','Kandinsky'])
          player.otherGroupID3 = random.choice(['Klee','Kandinsky'])
    elif (player.treatment == 'identity4Groups' or 
      player.treatment == 'identity4GroupsLowThreshold'):
          player.otherGroupID1 = random.choice(['Klee','Kandinsky','Picasso','Chagall'])
          player.otherGroupID2 = random.choice(['Klee','Kandinsky','Picasso','Chagall'])
          player.otherGroupID3 = random.choice(['Klee','Kandinsky','Picasso','Chagall'])
    if (player.treatment!='noIdentity' and 
      player.treatment!='noIdentityLowThreshold'):
          player.participant.otherGroupID1 = player.otherGroupID1
          player.participant.otherGroupID2 = player.otherGroupID2
          player.participant.otherGroupID3 = player.otherGroupID3  
    player.participant.otherKleesIdentity = ['']
    player.participant.otherKandinskysIdentity = ['']
    player.participant.otherChagallsIdentity = ['']
    player.participant.otherPicassosIdentity = ['']
    return {
      'exchange_rate': round(player.session.config['real_world_currency_per_point']*100)
      }
      
  @staticmethod
  def before_next_page(player: Player,timeout_happened):
      player.participant.numStage = player.participant.numStage + 1
      player.participant.groupIDRandom2 = random.choice(['Klee','Kandinsky'])
      player.participant.groupIDRandom4 = random.choice(['Klee','Kandinsky','Chagall','Picasso'])
      player.participant.num_kleesRandom = random.randint(2,Constants.numPlayersConsidered)
      player.participant.klees_guessing_kleeRandom = random.randint(2,player.participant.num_kleesRandom)
      player.participant.num_kandinskysRandom = random.randint(2,Constants.numPlayersConsidered)
      player.participant.kandinskys_guessing_kleeRandom = random.randint(2,player.participant.num_kandinskysRandom)
      player.participant.num_chagallsRandom = random.randint(2,Constants.numPlayersConsidered)
      player.participant.chagalls_guessing_kleeRandom = random.randint(2,player.participant.num_chagallsRandom)
      player.participant.num_picassosRandom = random.randint(2,Constants.numPlayersConsidered)
      player.participant.picassos_guessing_kleeRandom = random.randint(2,player.participant.num_picassosRandom)
      player.participant.painterQuiz_payoff = random.choice([0,10])
      player.participant.painterQuiz_additionalPayoff = random.choice([0,10])
      player.participant.allA_payoffs1 = random.choice([15,10])
      player.participant.allA_payoffs2 = random.choice([15,10])
      player.participant.choiceNumForPayoff = random.choice([1,2])
      mu1 = Constants.endowment/2
      sigma1 = Constants.endowment/10
      player.participant.PGOtherChoice1 = round(np.random.randn()*sigma1+mu1)
      player.participant.PGOtherChoice2 = round(np.random.randn()*sigma1+mu1)
      player.participant.PGOtherChoice3 = round(np.random.randn()*sigma1+mu1)
      player.participant.riskGame1OtherChoice1 = random.choice(['A','B'])
      player.participant.riskGame1OtherChoice2 = random.choice(['A','B'])
      player.participant.riskGame1OtherChoice3 = random.choice(['A','B'])
      player.participant.riskGame2OtherChoice1 = random.choice(['A','B'])
      player.participant.riskGame2OtherChoice2 = random.choice(['A','B'])
      player.participant.riskGame2OtherChoice3 = random.choice(['A','B'])
      player.participant.choiceNumForPayoff = random.choice([1,2])  
      mu2 = 35
      sigma2 = 5
      player.participant.beautyOtherChoice1 = np.random.randn()*sigma2+mu2
      player.participant.beautyOtherChoice2 = np.random.randn()*sigma2+mu2
      player.participant.beautyOtherChoice3 = np.random.randn()*sigma2+mu2
      players = player.subsession.get_players() 
      for p in players: 
        p.participant.groupID = 'Not yet assigned'
      
page_sequence = [experimentIntroduction]    