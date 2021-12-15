from otree.api import *
import random
import json
import csv

#******************************************************************************#
# Constants
#******************************************************************************#
class Constants(BaseConstants):
    name_in_url = 'introduction'
    players_per_group = None
    num_rounds = 1  
    endowment = 5
    painterQuiz_reward = 5
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
    #player.treatment=random.choice(['noIdentity','identity','identity4Groups'])
    player.treatment=random.choice(['noIdentity','identity','identity','identity'])
    player.participant.treatment = player.treatment
    player.participant.treatmentThreshold1=random.choice([3,4])
    player.orderOfApps = random.choice([1,1,1,2])
    player.participant.orderOfApps = player.orderOfApps
    player.participant.numStage = 0
    if (player.treatment == 'noIdentity'):
          player.otherGroupID1 = random.choice(['Klee','Kandinsky'])
          player.otherGroupID2 = random.choice(['Klee','Kandinsky'])
          player.otherGroupID3 = random.choice(['Klee','Kandinsky'])
    player.participant.otherKleesIdentity = ['']
    player.participant.otherKandinskysIdentity = ['']
    player.participant.otherChagallsIdentity = ['']
    player.participant.otherPicassosIdentity = ['']
    return {
      'exchange_rate': round(player.session.config['real_world_currency_per_point']*100),
      'participation_fee': player.session.config['participation_fee']
      }
      
  @staticmethod
  def before_next_page(player: Player,timeout_happened):
      player.participant.numStage = player.participant.numStage + 1
      player.participant.groupIDRandom2 = random.choice(['Klee','Kandinsky'])
      player.participant.groupIDRandom4 = random.choice(['Klee','Kandinsky','Chagall','Picasso'])
      player.participant.groupCompositionRandomNumber = random.randint(0,100)
      player.participant.groupCompositionRandomNumber_1 = random.randint(1,3)
      player.participant.num_kleesRandom = random.randint(2,Constants.numPlayersConsidered)
      player.participant.klees_guessing_kleeRandom = random.randint(2,player.participant.num_kleesRandom)
      player.participant.num_kandinskysRandom = random.randint(2,Constants.numPlayersConsidered)
      player.participant.kandinskys_guessing_kleeRandom = random.randint(2,player.participant.num_kandinskysRandom)
      player.participant.num_chagallsRandom = random.randint(2,Constants.numPlayersConsidered)
      player.participant.chagalls_guessing_kleeRandom = random.randint(2,player.participant.num_chagallsRandom)
      player.participant.num_picassosRandom = random.randint(2,Constants.numPlayersConsidered)
      player.participant.picassos_guessing_kleeRandom = random.randint(2,player.participant.num_picassosRandom)
      player.participant.painterQuiz_payoff = random.choice([0,Constants.painterQuiz_reward])
      player.participant.painterQuiz_additionalPayoff = random.choice([0,Constants.painterQuiz_reward])
      player.participant.allA_payoffs1 = random.choice([15,10])
      player.participant.allA_payoffs2 = random.choice([15,10])
      player.participant.choiceNumForPayoff = random.choice([1,2])
      player.participant.PGOtherChoice1 = random.randint(0,Constants.endowment)
      player.participant.PGOtherChoice2 = random.randint(0,Constants.endowment)
      player.participant.PGOtherChoice3 = random.randint(0,Constants.endowment)
      player.participant.riskGame1OtherChoice1 = random.choice(['A','B'])
      player.participant.riskGame1OtherChoice2 = random.choice(['A','B'])
      player.participant.riskGame1OtherChoice3 = random.choice(['A','B'])
      player.participant.riskGame2OtherChoice1 = random.choice(['A','B'])
      player.participant.riskGame2OtherChoice2 = random.choice(['A','B'])
      player.participant.riskGame2OtherChoice3 = random.choice(['A','B'])
      player.participant.guess30 = random.choice(['AAA','AAA','AAA','Not AAA',
        'Not AAA','Not AAA','Not AAA','Not AAA','Not AAA','Not AAA'])
      player.participant.guess50 = random.choice(['AAA','Not AAA'])
      player.participant.guess70 = random.choice(['AAA','AAA','AAA','AAA','AAA',
        'AAA','AAA','Not AAA','Not AAA','Not AAA'])
      player.participant.beautyOtherChoice1 = random.randint(15,60)
      player.participant.beautyOtherChoice2 = random.randint(15,60)
      player.participant.beautyOtherChoice3 = random.randint(15,60)
      
page_sequence = [experimentIntroduction]    
