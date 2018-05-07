from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range, safe_json, 
)
import csv
import random
import math

from django import forms

author = 'Dominik Duell'

doc = """
group assignment based on self-reported important group markers or random draw
"""

class Constants(BaseConstants):
    name_in_url = 'groupAssignment'
    players_per_group = None
    num_rounds = 1
    num_rounds_stage_3 = 3
    
    quiz_player1_correct = c(0)
    quiz_player2_correct = c(0)
    quiz_maximum_offered_points = c(300)

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass
                
class Player(BasePlayer): 
    assignment_p1 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p2 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p3 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p4 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p5 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p6 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p7 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p8 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p9 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p10 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p11 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p12 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p13 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p14 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p15 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p16 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p17 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p18 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p19 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p20 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p21 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p22 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p23 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
    assignment_p24 = models.IntegerField(verbose_name='',initial=1,min=1,max=2)
         
    identity1 = models.StringField(verbose_name='',max_length=100)
    identity2 = models.StringField(verbose_name='',max_length=100)
                                    
    rdmNumber = models.FloatField()
    groupIDRaw = models.IntegerField(min=1,max=2)
    groupID = models.CharField()
    
    quiz_question_player1 = models.CurrencyField(min=0, max=Constants.quiz_maximum_offered_points)

    quiz_question_player2 = models.CurrencyField(min=0, max=Constants.quiz_maximum_offered_points)
    
    def is_training_question_player1_correct(self):
        return (self.training_question_1_player1 ==
                Constants.training_1_player1_correct)

    def is_training_question_black_correct(self):
        return (self.training_question_1_player2 ==
                Constants.training_1_player2_correct)

    def other_player(self):
        """Returns other player in group"""
        return self.get_others_in_group()[0]