from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from .validators import ValidateImageExtesion

# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User)
    friend = models.ManyToManyField('self', symmetrical=True,  blank=True)
    picture = models.FileField(upload_to='users/profile_images', validators = [ValidateImageExtesion], blank=True)
    def __unicode__(self):
        return self.user.username

