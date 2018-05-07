from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants

from django_countries import countries

import random


class PlayerBot(Bot):

    def play_round(self):
        yield (views.Demographics, {'age': random.randint(0,100),
                               'gender': random.randint(0,1),
                               'state': 'California',
                               'race': random.randint(1,3),
                               }
               )
