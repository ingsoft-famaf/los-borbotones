from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length = 30)
    description = models.CharField(max_length = 300)
    pub_date = models.DateTimeField('date_published', auto_now_add=True)
    def __str__(self):
        return self.title