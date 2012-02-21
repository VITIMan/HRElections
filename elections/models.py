# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Candidate(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre del partido")
    abbreviation = models.CharField(max_length=255, verbose_name=u"Siglas del partido")
    description = models.TextField(help_text="Descripción del partido")
    image = models.URLField(default='',verbose_name="Url de la imagen")
    #email = models.EmailField()
    user = models.ForeignKey(User, unique=True)
    published_at = models.DateTimeField(auto_now_add = True, help_text="Fecha de publicación")

#class Image(models.Model):
#    candidate = models.ForeignKey(Candidate)
#    url = models.URLField(default = '', help_text= "Url de la imagen")
#    type = models.CharField(max_length=255, verbose_name="Tipo, vídeo o imagen")

class Comment(models.Model):
    candidate = models.ForeignKey(Candidate)
    name = models.CharField(max_length=255, verbose_name="Autor")
    text = models.TextField(help_text="Comentario")
    published_at = models.DateTimeField(auto_now_add = True, help_text="Fecha de publicación")
    ip = models.CharField(max_length=255, verbose_name="IP")

class Votes(models.Model):
    candidate = models.ForeignKey(Candidate)
    stars = IntegerRangeField(min_value=1, max_value=5, verbose_name='Puntuación')
    ip = models.CharField(max_length=255, verbose_name="IP") #una IP por candidato pero puedes votar a todos los candidatos. Sólo por el mismo día????
    voted_at = models.DateTimeField(auto_now_add = True, help_text="Fecha de publicación")

class Ranking(models.Model):
    candidate = models.ForeignKey(Candidate)
    stars = models.BigIntegerField( default=0)
    avg = models.FloatField(default=0)
    votes = models.BigIntegerField(default=0)
    avg_points = models.FloatField(default=0)
    votes_points = models.FloatField(default=0)
    published_at = models.DateTimeField(auto_now_add = True, help_text="Fecha de publicación")
    ranking = models.IntegerField(default=0)
