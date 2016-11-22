from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from videos.models import Video
from .validators import ValidateImageExtesion

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    friends = models.ManyToManyField('self', symmetrical=True,  blank=True)
    picture = models.FileField(upload_to='users/profile_images', validators = [ValidateImageExtesion], blank=True)
    def __unicode__(self):
        return self.user.username

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    def __str__(self):
        return "From: {} To: {}".fromat(self.sender.username, self.receiver.username)
        

