from django.db import models

class Article(models.Model):
    journal = models.TextField()
    title = models.TextField()
    text = models.TextField()
    content = models.TextField()
    keys = models.TextField()

class DictItem(models.Model):
    ids = models.ManyToManyField(Article)
    word = models.TextField(primary_key=True)

class Passwd(models.Model):
    id = models.TextField(primary_key=True)
    passwd = models.TextField()