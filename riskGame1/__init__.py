from otree.api import *
import random
from decimal import Decimal

#******************************************************************************#
# Constants
#******************************************************************************#
class Constants(BaseConstants):
    name_in_url = 'riskGame1'
    players_per_group = None
    num_rounds = 1 
    quizQuestion1_correct = 4
    quizQuestion2_correct = 12
    beliefElicitation_reward = 5

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
  playerInGame = models.IntegerField()
  choice1Done = models.CharField(initial='Not yet chosen')
  otherGroupID1 = models.CharField()
  otherGroupID2 = models.CharField()
  otherGroupID3 = models.CharField()
  allA_payoffs1 = models.IntegerField()
  allA_payoffs2 = models.IntegerField()
  otherChoice1 = models.CharField()
  otherChoice2 = models.CharField()
  otherChoice3 = models.CharField()
  riskGameOtherChoice1 = models.IntegerField()
  riskGameOtherChoice2 = models.IntegerField()
  riskGameOtherChoice3 = models.IntegerField()
  riskGame_payoffs = models.IntegerField(initial = 0)
  beliefElicitation_payoffs = models.IntegerField(initial = 0)
  choice1 = models.CharField(
      choices=['A', 'B'],
      widget=widgets.RadioSelect())
  choice2 = models.CharField(
      choices=['A', 'B'],
      widget=widgets.RadioSelect())
  quizQuestion1 = models.IntegerField(
      choices=[4,7,12,18],
      max_digits=2,
      widget=widgets.RadioSelectHorizontal())
  quizQuestion2 = models.IntegerField(
      choices=[4,7,12,18],
      max_digits=2,
      widget=widgets.RadioSelectHorizontal())
  belief1 = models.CharField(
      choices=[
        '10 out of 10 times (Always)','7 out of 10 times (Likely)',
        '5 out of 10 times (Neither likely nor unlikely)',
        '3 out of 10 times (Unlikely)','0 out of 10 times (Never)'],
      widget=widgets.RadioSelect())
  belief2 = models.CharField(
      choices=['10 out of 10 times (Always)','7 out of 10 times (Likely)',
        '5 out of 10 times (Neither likely nor unlikely)',
        '3 out of 10 times (Unlikely)','0 out of 10 times (Never)'],
      widget=widgets.RadioSelect())
  guess = models.CharField()
  treatmentThreshold1 = models.IntegerField()
  treatmentThreshold2 = models.IntegerField()
  treatmentThresholdForPayoff = models.IntegerField()
  choiceNumForPayoff = models.IntegerField()
  choiceForPayoff = models.CharField()
  beliefForPayoff = models.CharField()
  allA_payoffsForPayoff = models.IntegerField()
  feedback1 = models.TextField()
  
#******************************************************************************#
# Pages
#******************************************************************************#
# Risk game introduction
#*****************************************************************************#
class RiskGameIntroduction(Page):
    @staticmethod
    def is_displayed(player: Player):
      player.treatment = player.participant.treatment
      player.treatmentThreshold1 = player.participant.treatmentThreshold1
      player.numStage = player.participant.numStage
      player.allA_payoffs1 = player.participant.allA_payoffs1
      player.allA_payoffs2 = player.participant.allA_payoffs2
      
      if player.treatment != 'noIdentity':
        player.groupID = player.participant.groupID    
        player.otherGroupID1 = player.participant.otherGroupID1
        player.otherGroupID2 = player.participant.otherGroupID2
        player.otherGroupID3 = player.participant.otherGroupID3
        
      player.orderOfApps = player.participant.orderOfApps
      return player.orderOfApps==1 

#*****************************************************************************#
# Quiz
#*****************************************************************************#
class Quiz(Page):
    form_model = 'player'
    form_fields = ['quizQuestion1','quizQuestion2']
    
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
# Choice 1
#*****************************************************************************#
class Choice1(Page):
    form_model = 'player'
    form_fields = ['choice1','belief1']
        
    @staticmethod
    def is_displayed(player: Player):
      return player.orderOfApps==1 

#*****************************************************************************#
# Choice 2
#*****************************************************************************#
class Choice2(Page):
    form_model = 'player'
    form_fields = ['choice2','belief2']
    
    @staticmethod
    def is_displayed(player: Player):
      return player.orderOfApps==1 
    
    @staticmethod 
    def vars_for_template(player: Player): 
        if (player.treatmentThreshold1==4):
          player.treatmentThreshold2 = 3
        else: 
          player.treatmentThreshold2 = 4
     
    @staticmethod 
    def before_next_page(player: Player,timeout_happened): 
      player.choiceNumForPayoff = player.participant.choiceNumForPayoff
      if player.choiceNumForPayoff==1:
        player.treatmentThresholdForPayoff = player.treatmentThreshold1
        player.choiceForPayoff = player.choice1
        player.beliefForPayoff = player.belief1
        player.allA_payoffsForPayoff = player.allA_payoffs1
      else: 
        player.treatmentThresholdForPayoff = player.treatmentThreshold2
        player.choiceForPayoff = player.choice2
        player.beliefForPayoff = player.belief2
        player.allA_payoffsForPayoff = player.allA_payoffs2
     
#*****************************************************************************#
# Results
#*****************************************************************************#
class Results(Page):
    form_model = 'player'
    form_fields = ['feedback1']
    
    @staticmethod
    def is_displayed(player: Player):
      return player.orderOfApps==1
    
    @staticmethod 
    def vars_for_template(player: Player):
      players = player.subsession.get_players()
      playersDone = [p for p in players if p.choice1Done!='Not yet chosen']
      if player.participant.treatment!='noIdentity':
          klees = [p for p in playersDone if p.groupID == 'Klee']
          kandinskys = [p for p in playersDone if p.groupID == 'Kandinsky']
          chagalls = [p for p in playersDone if p.groupID == 'Chagall']
          picassos = [p for p in playersDone if p.groupID == 'Picasso']
        
      # No identity treatment
      if player.participant.treatment=='noIdentity':
          if len(playersDone)>2:
            if player.choiceNumForPayoff==1:
              player.otherChoice1 = playersDone[-1].choice1
              player.otherChoice2 = playersDone[-2].choice1
              player.otherChoice3 = playersDone[-3].choice1
            else:
              player.otherChoice1 = playersDone[-1].choice2
              player.otherChoice2 = playersDone[-2].choice2
              player.otherChoice3 = playersDone[-3].choice2
          elif len(playersDone)==2:
            if player.choiceNumForPayoff==1:
              player.otherChoice1 = playersDone[-1].choice1
              player.otherChoice2 = playersDone[-2].choice1
            else:
              player.otherChoice1 = playersDone[-1].choice2
              player.otherChoice2 = playersDone[-2].choice2
            player.otherChoice3 = player.participant.riskGame1OtherChoice3 
          elif len(playersDone)==1:
            if player.choiceNumForPayoff==1:
              player.otherChoice1 = playersDone[-1].choice1
            else:
              player.otherChoice1 = playersDone[-1].choice2
            player.otherChoice2 = player.participant.riskGame1OtherChoice2
            player.otherChoice3 = player.participant.riskGame1OtherChoice3   
          else:
            player.otherChoice1 = player.participant.riskGame1OtherChoice1
            player.otherChoice2 = player.participant.riskGame1OtherChoice2 
            player.otherChoice3 = player.participant.riskGame1OtherChoice3 
      
      else:  
        # Identity treatments
        if (player.otherGroupID1=="Klee"):
          if (len(klees)>0):
            if player.choiceNumForPayoff==1:
              player.otherChoice1 = klees[-1].choice1
            else:
              player.otherChoice1 = klees[-1].choice2
          else:
            player.otherChoice1 = player.participant.riskGame1OtherChoice1 
        elif (player.otherGroupID1=="Kandinsky"):
          if (len(kandinskys)>0):
            if player.choiceNumForPayoff==1:
              player.otherChoice1 = kandinskys[-1].choice1
            else:
              player.otherChoice1 = kandinskys[-1].choice2
          else:
            player.otherChoice1 = player.participant.riskGame1OtherChoice1   
        elif (player.otherGroupID1=="Chagall"):
          if (len(chagalls)>0):
            if player.choiceNumForPayoff==1:
              player.otherChoice1 = chagalls[-1].choice1
            else:
              player.otherChoice1 = chagalls[-1].choice2
          else:
            player.otherChoice1 = player.participant.riskGame1OtherChoice1   
        elif (player.otherGroupID1=="Picasso"):
          if (len(picassos)>0):
            if player.choiceNumForPayoff==1:
              player.otherChoice1 = chagalls[-1].choice1
            else:
              player.otherChoice1 = chagalls[-1].choice2
          else:
            player.otherChoice1 = player.participant.riskGame1OtherChoice1  

        if (player.otherGroupID2=="Klee"):
          if (len(klees)>1):
            if player.choiceNumForPayoff==1:
              player.otherChoice2 = klees[-1].choice1
            else:
              player.otherChoice2 = klees[-1].choice2
          else:
            player.otherChoice2 = player.participant.riskGame1OtherChoice2 
        elif (player.otherGroupID2=="Kandinsky"):
          if (len(kandinskys)>1):
            if player.choiceNumForPayoff==1:
              player.otherChoice2 = kandinskys[-1].choice1
            else:
              player.otherChoice2 = kandinskys[-1].choice2
          else:
            player.otherChoice2 = player.participant.riskGame1OtherChoice2   
        elif (player.otherGroupID2=="Chagall"):
          if (len(chagalls)>0):
            if player.choiceNumForPayoff==1:
              player.otherChoice2 = chagalls[-1].choice1
            else:
              player.otherChoice2 = chagalls[-1].choice2
          else:
            player.otherChoice2 = player.participant.riskGame1OtherChoice2   
        elif (player.otherGroupID2=="Picasso"):
          if (len(picassos)>0):
            if player.choiceNumForPayoff==1:
              player.otherChoice2 = picassos[-1].choice1
            else:
              player.otherChoice2 = picassos[-1].choice2
          else:
            player.otherChoice2 = player.participant.riskGame1OtherChoice2 
 
        if (player.otherGroupID3=="Klee"):
          if (len(klees)>1):
            if player.choiceNumForPayoff==1:
              player.otherChoice3 = klees[-1].choice1
            else:
              player.otherChoice3 = klees[-1].choice2
          else:
            player.otherChoice3 = player.participant.riskGame1OtherChoice3 
        elif (player.otherGroupID3=="Kandinsky"):
          if (len(kandinskys)>1):
            if player.choiceNumForPayoff==1:
              player.otherChoice3 = kandinskys[-1].choice1
            else:
              player.otherChoice3 = kandinskys[-1].choice2
          else:
            player.otherChoice3 = player.participant.riskGame1OtherChoice3   
        elif (player.otherGroupID3=="Chagall"):
          if (len(chagalls)>0):
            if player.choiceNumForPayoff==1:
              player.otherChoice3 = chagalls[-1].choice1
            else:
              player.otherChoice3 = chagalls[-1].choice2
          else:
            player.otherChoice3 = player.participant.riskGame1OtherChoice3   
        elif (player.otherGroupID3=="Picasso"):
          if (len(picassos)>0):
            if player.choiceNumForPayoff==1:
              player.otherChoice3 = picassos[-1].choice1
            else:
              player.otherChoice3 = picassos[-1].choice2
          else:
            player.otherChoice3 = player.participant.riskGame1OtherChoice3 
      
      otherChoices = player.otherChoice1 + player.otherChoice2 + player.otherChoice3
      # A,A top left  
      if player.allA_payoffsForPayoff==15:
        if (player.treatmentThresholdForPayoff==4):
          if player.choiceForPayoff=='A':
            if otherChoices=='AAA':
              payoff = 15
            else: 
              payoff = 0
          else:
            if otherChoices=='BBB':
              payoff = 10
            else: 
              payoff = 8
        else:
          if player.choiceForPayoff=='A':
            if (otherChoices=='AAA' or otherChoices=='AAB' or 
                otherChoices=='ABA' or otherChoices=='BAA'):
              payoff = 15
            else: 
              payoff = 0
          else:
            if (otherChoices=='BBB' or otherChoices=='BBA' or 
                otherChoices=='BAB' or otherChoices=='BBA'):
              payoff = 10
            else: 
              payoff = 8
      # B,B top left  
      else:
        if (player.treatmentThresholdForPayoff==4):
          if player.choiceForPayoff=='B':
            if otherChoices=='BBB':
              payoff = 15
            else: 
              payoff = 0
          else:
            if otherChoices=='AAA':
              payoff = 10
            else: 
              payoff = 8
        else:
          if player.choiceForPayoff=='B':
            if (otherChoices=='BBB' or otherChoices=='BBA' or 
                otherChoices=='BAB' or otherChoices=='ABB'):
              payoff = 15
            else: 
              payoff = 0
          else:
            if (otherChoices=='AAA' or otherChoices=='AAB' or 
                otherChoices=='ABA' or otherChoices=='BAA'):
              payoff = 10
            else: 
              payoff = 8
      
      if player.beliefForPayoff=='10 out of 10 times (Always)':
        player.guess = 'AAA'
      elif player.beliefForPayoff=='7 out of 10 times (Likely)':
        player.guess = player.participant.guess50
      elif player.beliefForPayoff=='5 out of 10 times (Neither likely nor unlikely)':
        player.guess = player.participant.guess70
      elif player.beliefForPayoff=='3 out of 10 times (Unlikely)':
        player.guess = player.participant.guess30
      else:
        player.guess = 'Not AAA'
      
      if ((otherChoices=='AAA' and player.guess=='AAA') or
      (otherChoices!='AAA' and player.guess=='Not AAA')):
        player.beliefElicitation_payoffs = Constants.beliefElicitation_reward   
      else:
        player.beliefElicitation_payoffs = 0  
      
      if player.beliefForPayoff=='10 out of 10 times (Always)':
        beliefForPayoffDisplay = '10 out of 10 times'
      elif player.beliefForPayoff=='7 out of 10 times (Likely)':
        beliefForPayoffDisplay = '7 out of 10 times'
      elif player.beliefForPayoff=='5 out of 10 times (Neither likely nor unlikely)':
        beliefForPayoffDisplay = '5 out of 10 times'
      elif player.beliefForPayoff=='3 out of 10 times (Unlikely)':
        beliefForPayoffDisplay = '3 out of 10 times'
      else: 
        beliefForPayoffDisplay = '0 out of 10 times'
      player.riskGame_payoffs = payoff 
      player.participant.riskGame_payoffs = (player.riskGame_payoffs + 
        player.beliefElicitation_payoffs)
        
      return {
            'nextStage': player.numStage + 1,
            'totalPayoffs': player.participant.riskGame_payoffs,
            'beliefForPayoffDisplay': beliefForPayoffDisplay
        }
        
    @staticmethod
    def before_next_page(player: Player,timeout_happened):
      player.participant.numStage = player.participant.numStage + 1
                 
#*****************************************************************************#
                             
page_sequence = [
    RiskGameIntroduction,
    Quiz,
    QuizFeedback,
    Choice1,
    Choice2,
    Results
]
