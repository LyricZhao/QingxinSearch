from django.db import models

class Article(models.Model):
    id = models.IntegerField(primary_key=True)
    journal = models.TextField()
    title = models.TextField()
    content = models.TextField()
    keys = models.TextField()

    def as_dict(self):
        return {
            'journal': self.journal,
            'title': self.title,
            'content': self.content,
            'keys': self.keys
        }

class DictItem(models.Model):
    ids = models.ManyToManyField(Article)
    word = models.TextField()

class Passwd(models.Model):
    id = models.TextField(primary_key=True)
    passwd = models.TextField()