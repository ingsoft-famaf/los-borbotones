from __future__ import unicode_literals

from django.db import models
from .validators import validate_file_extension
# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length = 30)
    description = models.CharField(max_length = 300)
    pub_date = models.DateTimeField('date_published', auto_now_add=True)
    file = models.FileField(upload_to='videos/%Y/%m/%d/',validators = [validate_file_extension])
    #autor = models.ForeignKey('User', on_delete=models.SET_DEFAULT, default="None")

    def __str__(self):
        return self.title