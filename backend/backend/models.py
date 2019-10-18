from django.db import models
from django.contrib import admin

class DictItem(models.Model):
    word = models.TextField()
    id = models.IntegerField()

class Article(models.Model):
    id = models.IntegerField()
    journal = models.TextField()
    title = models.TextField()
    content = models.TextField()
    keys = models.TextField()


