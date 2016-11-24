from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from .validators import validate_file_extension
# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length = 80)
    description = models.TextField(max_length = 800)
    pub_date = models.DateTimeField('date_published', auto_now_add=True)
    file = models.FileField(upload_to='videos/%Y/%m/%d/',validators = [validate_file_extension])
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
