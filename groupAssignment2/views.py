from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class identityQuestion(Page):
    form_model = 'player'
    form_fields = ['identity1','identity2']
    
    def is_displayed(self):
        return self.player.id_in_group > 2

    def before_next_page(self):
        for p in self.subsession.get_players():
            p.participant.vars['identity1'] = self.player.identity1
            p.participant.vars['identity2'] = self.player.identity2

class identityAssignmentWaitPage(WaitPage):
    def after_all_players_arrive(self):
        return True
        
class identityAssignment(Page):
    form_model = 'player'
    form_fields = [ 'assignment_p1', 'assignment_p2', 'assignment_p3',
                    'assignment_p4', 'assignment_p5', 'assignment_p6',
                    'assignment_p7', 'assignment_p8', 'assignment_p9',
                    'assignment_p10', 'assignment_p11', 'assignment_p12',
                    'assignment_p13', 'assignment_p14', 'assignment_p15',
                    'assignment_p16', 'assignment_p17', 'assignment_p18',
                    'assignment_p19', 'assignment_p20', 'assignment_p21',
                    'assignment_p22', 'assignment_p23', 'assignment_p24']
    
    def is_displayed(self):
        return self.player.id_in_group < 3
        
    def vars_for_template(self):   
        for p in self.subsession.get_players():
            p.player_id = p.id_in_group - 2           
        
        num_players = len(self.player.get_others_in_group()) - 1
        players = [p for p in self.subsession.get_players() if p.id_in_group > 2]
        
        return{
            'players': players,
            'num_players': num_players,
            'player_id': self.player.player_id
        }
        
    def before_next_page(self):   
        players = [p for p in self.subsession.get_players() if p.id_in_group > 2]          
        i = 1
        for p in players:
            assignment = 'p.get_others_in_group()[0].assignment_p'
            assignment +=str(i)
            p.groupIDRaw = eval(assignment)
            i = i+1    
        
        players = [p for p in self.subsession.get_players() if p.id_in_group < 3]  
        for p in players:
            self.player.groupID = random.choice(['Green','Blue'])
            p.participant.vars['groupID'] = p.groupID  
                                                                
class Introduction(Page):
    timeout_seconds = 300
    
    def is_displayed(self):
        return self.player.id_in_group > 2
        
    def before_next_page(self):
        self.player.rdmNumber = random.random()
        
        if self.player.rdmNumber > .01:
            self.player.groupID = random.choice(['Green','Blue'])
            
        else:
            if self.player.groupIDRaw == 1:
                self.player.groupID = 'Green'
            else: 
                self.player.groupID = 'Blue'
                
        for p in self.subsession.get_players():
            p.participant.vars['groupID'] = p.groupID        

							
class Quiz(Page):
    def is_displayed(self):
        return self.player.id_in_group > 2

    form_model = models.Player
    form_fields = ['quiz_question_player1','quiz_question_player2']

    def vars_for_template(self):
        return {'num_q': 1}

class QuizFeedback(Page):
    def is_displayed(self):
        return self.player.id_in_group > 2

    def vars_for_template(self):
        return {
            'num_q': 1,
               }  
               
class QuziWaitPage(WaitPage): 
    def after_all_players_arrive(self):
        pass
                               
page_sequence = [
    identityQuestion,
    identityAssignmentWaitPage,
    identityAssignment,
    Introduction,
    Quiz,
    QuizFeedback,
    QuziWaitPage
]
