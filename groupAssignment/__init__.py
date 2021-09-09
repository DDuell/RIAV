from otree.api import *
import random
from decimal import Decimal
from otree.lookup import url_i_should_be_on, get_page_lookup, get_min_idx_for_app
from fuzzywuzzy import fuzz

#******************************************************************************#
# Constants
#******************************************************************************#
class Constants(BaseConstants):
    name_in_url = 'painterQuiz'
    players_per_group = None
    num_rounds = 1  
    painterQuiz_reward = 10
    painterQuiz_answer = 0 # Kandinsky
    
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
    playerInSession = models.IntegerField()
    identity1 = models.StringField(verbose_name='',max_length=100,label='')
    identity2 = models.StringField(verbose_name='',max_length=100,label='')
    groupID = models.CharField(initial='Not assigned yet')
    matchRatioKlees = models.IntegerField(initial=0)
    matchRatioKandinskys = models.IntegerField(initial=0)
    matchRatioChagalls = models.IntegerField(initial=0)
    matchRatioPicassos = models.IntegerField(initial=0)
    guess = models.PositiveIntegerField(
        label='',
        initial=None,
        choices=[(1, 'Klee'), (0, 'Kandinsky'),],
        verbose_name='',
        widget=widgets.RadioSelectHorizontal()
    )    
    help = models.PositiveIntegerField(
        label='',
        initial=None,
        choices=[(1, 'Yes'), (0, 'No'),],
        verbose_name='',
        widget=widgets.RadioSelectHorizontal()
    )   
    answer = models.IntegerField(
        label='',
        initial=None, 
        choices=[(1, 'Klee'), (0, 'Kandinsky'), ],
        widget=widgets.RadioSelectHorizontal()
    )  
     
    painterQuiz_payoff = models.IntegerField(initial=0)
    painterQuiz_additionalPayoff = models.IntegerField()
    painterQuiz_totalPayoff = models.IntegerField()
    otherGroupID1 = models.CharField()
    otherGroupID2 = models.CharField()
    otherGroupID3 = models.CharField()
    num_klees = models.PositiveIntegerField(initial=1)
    klees_guessing_klee = models.PositiveIntegerField(initial=1)
    klees_guessing_kandinsky = models.PositiveIntegerField(initial=1)
    num_kandinskys = models.PositiveIntegerField(initial=1)
    kandinskys_guessing_klee = models.PositiveIntegerField(initial=1)
    kandinskys_guessing_kandinsky = models.PositiveIntegerField(initial=1) 
    num_chagalls = models.PositiveIntegerField(initial=1)
    chagalls_guessing_klee = models.PositiveIntegerField(initial=1)
    chagalls_guessing_kandinsky = models.PositiveIntegerField(initial=1) 
    num_picassos = models.PositiveIntegerField(initial=1)
    picassos_guessing_klee = models.PositiveIntegerField(initial=1)
    picassos_guessing_kandinsky = models.PositiveIntegerField(initial=1) 
    percentage_klee = models.FloatField(initial=1) 
    percentage_kandinsky = models.FloatField(initial=1) 
    correct_klees = models.PositiveIntegerField(initial=1)
    correct_kandinskys = models.PositiveIntegerField(initial=1)
    correct_chagalls = models.PositiveIntegerField(initial=1)
    correct_picassos = models.PositiveIntegerField(initial=1)
    klees_payoff = models.IntegerField() 
    kandinskys_payoff = models.IntegerField() 
    chagalls_payoff = models.IntegerField() 
    picassos_payoff = models.IntegerField() 
      
#******************************************************************************#
# Pages
#******************************************************************************#
# Identity question
#*****************************************************************************#
class identityQuestion(Page):
    timeout_seconds = 120
    form_model = 'player'
    form_fields = ['identity1','identity2']
    
    @staticmethod
    def is_displayed(player: Player): 
        return (player.participant.treatment != 'noIdentity' and
          player.participant.treatment != 'noIdentityLowThreshold')
          
    @staticmethod    
    def vars_for_template(player: Player):
        player.treatment = player.participant.treatment
        player.matchRatioKlees = 0
        player.matchRatioKandinskys = 0
        player.matchRatioChagalls = 0
        player.matchRatioPicassos = 0
        players = player.subsession.get_players()
        player.playerInSession=len([p for p in players if p.groupID!='Not assigned yet']) + 1
        player.participant.playerInSession = player.playerInSession
    
    @staticmethod        
    def before_next_page(player: Player, timeout_happened):
        player.participant.identity = [player.identity1,player.identity2]
        players = player.subsession.get_players()
        playersWithGroupID=[p for p in players if p.groupID!='Not assigned yet']
        if player.playerInSession > 1:
          klees = [p for p in playersWithGroupID if p.groupID == 'Klee']
          kandinskys = [p for p in playersWithGroupID if p.groupID == 'Kandinsky']
          chagalls = [p for p in playersWithGroupID if p.groupID == 'Chagall']
          picassos = [p for p in playersWithGroupID if p.groupID == 'Picasso']
          for p in klees:
            player.participant.otherKleesIdentity.append(p.participant.identity)
          for p in kandinskys:
            player.participant.otherKandinskysIdentity.append(p.participant.identity)
          for p in chagalls:
            player.participant.otherChagallsIdentity.append(p.participant.identity)
          for p in picassos:
            player.participant.otherPicassosIdentity.append(p.participant.identity)
          for p in playersWithGroupID:
            if p.groupID !='Not assigned yet':
              print('others identity',p.participant.identity)
          # Treatments with groups of 2
          if len(klees) > 0:
            player.matchRatioKlees = fuzz.token_set_ratio(
              player.participant.otherKleesIdentity,player.participant.identity)
          if len(kandinskys) > 0:
            player.matchRatioKandinskys = fuzz.token_set_ratio(
              player.participant.otherKandinskysIdentity,player.participant.identity)
          if len(chagalls) > 0:
            player.matchRatioChagalls = fuzz.token_set_ratio(
              player.participant.otherChagallsIdentity,player.participant.identity)
          if len(picassos) > 0:
            player.matchRatioPicassos = fuzz.token_set_ratio(
              player.participant.otherPicassosIdentity,player.participant.identity)
          
          # Find closest identity match in treatment with 2 groups
          if (player.treatment == 'identity' or player.treatment == 'identityLowThreshold'):
            if player.matchRatioKlees > 50 and player.matchRatioKandinskys < 50:
                player.participant.groupID = 'Klee'
            elif player.matchRatioKlees < 50 and player.matchRatioKandinskys > 50: 
                player.participant.groupID = 'Kandinsky'
            else: 
                player.participant.groupID = player.participant.groupIDRandom2
          
          # Find closest identity match in treatment with 4 groups     
          if (player.treatment == 'identity4Groups' or player.treatment == 'identityLowThreshold4Groups'):
            if (player.matchRatioKlees > 50 and player.matchRatioKandinskys < 50
              and player.matchRatioChagalls < 50 and player.matchRatioPicassos < 50):
                player.participant.groupID = 'Klee'
            elif (player.matchRatioKlees < 50 and player.matchRatioKandinskys > 50
              and player.matchRatioChagalls < 50 and player.matchRatioPicassos < 50): 
                player.participant.groupID = 'Kandinsky'
            elif (player.matchRatioKlees < 50 and player.matchRatioKandinskys < 50
              and player.matchRatioChagalls > 50 and player.matchRatioPicassos < 50): 
                player.participant.groupID = 'Chagall'
            elif (player.matchRatioKlees < 50 and player.matchRatioKandinskys < 50
              and player.matchRatioChagalls > 50 and player.matchRatioPicassos < 50): 
                player.participant.groupID = 'Picasso'
            else: 
                player.participant.groupID = player.participant.groupIDRandom4
        else: 
          if (player.treatment == 'identity' or player.treatment == 'identityLowThreshold'):
            player.participant.groupID = player.participant.groupIDRandom2
          elif (player.treatment == 'identity4Groups' or player.treatment == 'identity4GroupsLowThreshold'):
            player.participant.groupID = player.participant.groupIDRandom4

        player.groupID = player.participant.groupID
        player.participant.identity1 = player.identity1
        player.participant.identity2 = player.identity2
 
# ******************************************************************************************************************** #
# Identity announcement
# ******************************************************************************************************************** #
class identityAnnouncement(Page):
    @staticmethod
    def is_displayed(player: Player): 
        return (player.participant.treatment != 'noIdentity' and player.participant.treatment != 'noIdentityLowThreshold')
          
# ******************************************************************************************************************** #
# Identity announcement 2
# ******************************************************************************************************************** #
class identityAnnouncement2(Page):
    @staticmethod
    def is_displayed(player: Player): 
      return (player.participant.treatment != 'noIdentity' and player.participant.treatment != 'noIdentityLowThreshold')
          
    @staticmethod    
    def vars_for_template(player: Player):
      return {
            'groupID': player.groupID,
        } 
        
# ******************************************************************************************************************** #
# Guess 
# ******************************************************************************************************************** #
class guess(Page):
    form_model = 'player'
    form_fields = ['guess','help']
    
    @staticmethod
    def is_displayed(player: Player): 
        return (player.participant.treatment != 'noIdentity' and
          player.participant.treatment != 'noIdentityLowThreshold')
    
#*****************************************************************************#
# Answer 
#*****************************************************************************#
class answer(Page):
    form_model = 'player'
    form_fields = ['answer']
    
    @staticmethod
    def is_displayed(player: Player): 
        return (player.participant.treatment != 'noIdentity' and
          player.participant.treatment != 'noIdentityLowThreshold')
    
    @staticmethod
    def vars_for_template(player: Player):  
        players = player.subsession.get_players()
        playersWithGroupID=[p for p in players if p.groupID!='Not assigned yet']
        if player.playerInSession > 1:
          klees = [p for p in playersWithGroupID if p.groupID == 'Klee']
          kandinskys = [p for p in playersWithGroupID if p.groupID == 'Kandinsky']
          chagalls = [p for p in playersWithGroupID if p.groupID == 'Chagall']
          picassos = [p for p in playersWithGroupID if p.groupID == 'Picasso']
        
          if len(klees) > 1: 
            player.num_klees = len(klees)
            player.klees_guessing_klee = len([p for p in klees if p.guess == 1])
            player.klees_guessing_kandinsky = len([p for p in klees if p.guess == 0])
          else:
            player.num_klees = player.participant.num_kleesRandom
            player.klees_guessing_klee = player.participant.klees_guessing_kleeRandom
            player.klees_guessing_kandinsky = player.num_klees-player.klees_guessing_klee
            
          if len(kandinskys) > 1:    
            player.num_kandinskys = len(kandinskys)
            player.kandinskys_guessing_klee = len([p for p in kandinskys if p.guess == 1])
            player.kandinskys_guessing_kandinsky = len([p for p in kandinskys if p.guess == 0]) 
          else:
            player.num_kandinskys = player.participant.num_kandinskysRandom
            player.kandinskys_guessing_klee = player.participant.kandinskys_guessing_kleeRandom
            player.kandinskys_guessing_kandinsky = player.num_kandinskys-player.klees_guessing_klee 
            
          if len(chagalls) > 1:    
            player.num_chagalls = len(chagalls)
            player.chagalls_guessing_klee = len([p for p in chagalls if p.guess == 1])
            player.chagalls_guessing_kandinsky = len([p for p in chagalls if p.guess == 0]) 
          else:
            player.num_chagalls = player.participant.num_chagallsRandom
            player.chagalls_guessing_klee =  player.participant.chagalls_guessing_kleeRandom
            player.chagalls_guessing_kandinsky = player.num_chagalls-player.klees_guessing_klee
            
          if len(picassos) > 1:    
            player.num_picassos = len(picassos)
            player.picassos_guessing_klee = len([p for p in picassos if p.guess == 1])
            player.picassos_guessing_kandinsky = len([p for p in picassos if p.guess == 0]) 
          else:
            player.num_picassos = player.participant.num_picassosRandom 
            player.picassos_guessing_klee = player.participant.picassos_guessing_kleeRandom
            player.picassos_guessing_kandinsky = player.num_picassos-player.klees_guessing_klee     
        
          if player.groupID == 'Klee':
            player.percentage_klee = (player.klees_guessing_klee/player.num_klees)*100
            player.percentage_kandinsky = (player.klees_guessing_kandinsky/player.num_klees)*100
          elif player.groupID == 'Kandinsky':
            player.percentage_klee = (player.kandinskys_guessing_klee/player.num_kandinskys)*100
            player.percentage_kandinsky = (player.kandinskys_guessing_kandinsky/player.num_kandinskys)*100 
          elif player.groupID == 'Chagall':
            player.percentage_klee = (player.chagalls_guessing_klee/player.num_chagalls)*100
            player.percentage_kandinsky = (player.chagalls_guessing_kandinsky/player.num_chagalls)*100  
          elif player.groupID == 'Picasso':
            player.percentage_klee = (player.picassos_guessing_klee/player.num_picassos)*100
            player.percentage_kandinsky = (player.picassos_guessing_kandinsky/player.num_picassos)*100      
        
        else:
          player.percentage_klee = 60
          player.percentage_kandinsky = 40
        
        player.percentage_klee = round(player.percentage_klee)
        player.percentage_kandinsky = round(player.percentage_kandinsky)

#*****************************************************************************#
# Results 
#*****************************************************************************#
class results(Page):
    
    @staticmethod
    def is_displayed(player: Player):
        return (player.participant.treatment != 'noIdentity' and
          player.participant.treatment != 'noIdentityLowThreshold')
       
    @staticmethod   
    def vars_for_template(player: Player):
        players = player.subsession.get_players()  
        playersWithGroupID=[p for p in players if p.groupID!='Not assigned yet']
        if player.playerInSession > 1:
          klees = [p for p in playersWithGroupID if p.groupID == 'Klee']
          kandinskys = [p for p in playersWithGroupID if p.groupID == 'Kandinsky'] 
          chagalls = [p for p in playersWithGroupID if p.groupID == 'Chagall']
          picassos = [p for p in playersWithGroupID if p.groupID == 'Picasso']
        
          if len(klees) > 1:
            num_klees_half = len(klees)/2
          else:
            num_klees_half = 1
        
          if len(kandinskys) > 1:       
            num_kandinskys_half = len(kandinskys)/2
          else:
            num_kandinskys_half = 1
            
          if len(chagalls) > 1:       
            num_chagalls_half = len(chagalls)/2
          else:
            num_chagalls_half = 1
            
          if len(picassos) > 1:       
            num_picassos_half = len(picassos)/2
          else:
            num_picassos_half = 1    
        
          if player.groupID == 'Klee':
            player.correct_klees = len([p for p in klees if p.answer == Constants.painterQuiz_answer])
            if player.correct_klees >= num_klees_half:
              player.painterQuiz_payoff = Constants.painterQuiz_reward
            elif player.correct_klees < num_klees_half:
              player.painterQuiz_payoff = 0
          if (player.participant.treatment!='identity4Groups' and 
            player.participant.treatment!='identity4GroupsLowThreshold'):
            if player.correct_klees >= player.correct_kandinskys:
              player.painterQuiz_additionalPayoff = Constants.painterQuiz_reward
            else:
              player.painterQuiz_additionalPayoff = 0
          elif(player.participant.treatment=='1' or
            player.participant.treatment=='identity4GroupsLowThreshold'):   
            if (player.correct_klees >= player.correct_kandinskys and
              player.correct_klees >= player.correct_chagalls and 
              player.correct_klees >= player.correct_picassos):
              player.painterQuiz_additionalPayoff = Constants.painterQuiz_reward
            else:
              player.painterQuiz_additionalPayoff = 0
        
          elif player.groupID == 'Kandinsky':
            player.correct_kandinskys = len([p for p in kandinskys if p.answer == Constants.painterQuiz_answer])
            if player.correct_kandinskys >= num_kandinskys_half:
              player.painterQuiz_payoff = Constants.painterQuiz_reward
            elif player.correct_kandinskys < num_kandinskys_half:
              player.painterQuiz_payoff = 0
            if (player.participant.treatment!='identity4Groups' and 
              player.participant.treatment!='identity4GroupsLowThreshold'):
              if player.correct_kandinskys >= player.correct_klees:
                player.painterQuiz_additionalPayoff = Constants.painterQuiz_reward
              else:
                player.painterQuiz_additionalPayoff = 0
            elif(player.participant.treatment=='identity4Groups' or
              player.participant.treatment=='identity4GroupsLowThreshold'):   
              if (player.correct_kandinskys >= player.correct_klees and
                player.correct_kandinskys >= player.correct_chagalls and 
                player.correct_kandinskys >= player.correct_picassos):
                player.painterQuiz_additionalPayoff = Constants.painterQuiz_reward
              else:
                player.painterQuiz_additionalPayoff = 0
        
          elif player.groupID == 'Chagall':
            player.correct_chagalls = len([p for p in chagalls if p.answer == Constants.painterQuiz_answer])
            if player.correct_chagalls >= num_chagalls_half:
              player.painterQuiz_payoff = Constants.painterQuiz_reward
            elif player.correct_chagalls < num_chagalls_half:
              player.painterQuiz_payoff = 0
            if (player.correct_chagalls >= player.correct_klees and
              player.correct_chagalls >= player.correct_kandinskys and
              player.correct_chagalls >= player.correct_picassos):
              player.painterQuiz_additionalPayoff = Constants.painterQuiz_reward
            else:
              player.painterQuiz_additionalPayoff = 0

          elif player.groupID == 'Picasso':
            player.correct_picassos = len([p for p in picassos if p.answer == Constants.painterQuiz_answer])
            if player.correct_picassos >= num_picassos_half:
              player.painterQuiz_payoff = Constants.painterQuiz_reward
            elif player.correct_chagalls < num_picassos_half:
              player.painterQuiz_payoff = 0
            if (player.correct_picassos >= player.correct_klees and
              player.correct_picassos >= player.correct_kandinskys and
              player.correct_picassos >= player.correct_chagalls):
              player.painterQuiz_additionalPayoff = Constants.painterQuiz_reward
            else:
              player.painterQuiz_additionalPayoff = 0
          
        else:
          player.painterQuiz_payoff = player.participant.painterQuiz_payoff
          player.painterQuiz_additionalPayoff = player.participant.painterQuiz_additionalPayoff
        
        player.painterQuiz_totalPayoff = player.painterQuiz_payoff + player.painterQuiz_additionalPayoff
        player.participant.painterQuiz_payoffs = player.painterQuiz_totalPayoff
  
    @staticmethod
    def before_next_page(player: Player,timeout_happened):
      player.participant.numStage = player.participant.numStage + 1

#*****************************************************************************#
#*****************************************************************************#
page_sequence = [
    identityQuestion,
    identityAnnouncement,
    identityAnnouncement2,
    guess,
    # help,
    answer,
    results
]
    
