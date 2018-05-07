from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Demographics(Page):

    form_model = models.Player

    form_fields = ['age','gender','race']

    def before_next_page(self):
        self.player.participant.vars['age'] = self.player.age
        self.player.participant.vars['gender'] = self.player.gender
        self.player.participant.vars['race'] = self.player.race
        
        self.player.rdmNumber = random.random()
        
        if self.player.rdmNumber > .01:
            self.player.groupID = random.choice(['A', 'B'])
            
        else:
            if self.player.rdmNumber <= .0033:
                if self.player.age < 50:
                    self.player.groupID = 'A'
                else:
                    self.player.groupID = 'B'
            elif (self.player.rdmNumber > .0033 and self.player.rdmNumber < .0066):
                if self.player.gender == 0:
                    self.player.groupID = 'A'
                else:
                    self.player.groupID = 'B'
            elif (self.player.rdmNumber > .0066 and self.player.rdmNumber < .01):
                if self.player.race == 1:
                    self.player.groupID = 'A'
                else:
                    self.player.groupID = 'B'

        for p in self.subsession.get_players():
            p.participant.vars['groupID'] = p.groupID 
            # if p.id_in_group  == 1:
          #       p.other_gender = self.group.gender_p2
          #   elif p.id_in_group  == 2:
          #       p.other_gender = self.group.gender_p1

        
page_sequence = [
    Demographics,
]
