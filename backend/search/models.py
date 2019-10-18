from django.db import models

# Create your models here.
class DictItem(models.Model):
    id = models.IntegerField(primary_key=True)
    word = models.TextField()

class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    journal = models.TextField()
    title = models.TextField()
    content = models.TextField()
    keys = models.TextField()

class Passwd(models.Model):
    id = models.TextField(primary_key=True)
    passwd = models.TextField()