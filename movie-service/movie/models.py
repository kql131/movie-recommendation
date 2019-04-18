# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255, null=False)
    director = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.title, self.director)

class List(models.Model):
    name=models.CharField(max_length=255, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    movies = models.ManyToManyField(Movie, blank=True)

class Tag(models.Model):
    movie=models.ManyToManyField(Movie, blank=True)
    name = models.CharField(max_length=255, null=False)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    rate = models.IntegerField()
