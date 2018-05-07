from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants

import random

class PlayerBot(Bot):
    def play_round(self):
        yield (views.Demographics, {
                'age': random.randint(18,75),
                'gender': random.randint(0,1),
                'state': 'CA',
                'race': random.randint(1,4)})
        yield (views.Introduction)
        yield (views.Screen1)
        if self.player.id_in_group == 1:
            yield (views.Screen2, {
                'demand': random.randint(1,7),
                'effort': random.randint(1,3)})
        if self.player.id_in_group == 2:
            yield (views.Screen3, {
                'choice': random.randint(0,1),
                'bonus':random.randint(0,1)})
        yield (views.Screen4)
        if self.player.round_number == Constants.num_rounds:
            yield (views.Results)
