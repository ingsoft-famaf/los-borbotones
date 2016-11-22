from __future__ import unicode_literals

from django.db import models

from videos.models import Video
from users.models import UserProfile

# Create your models here.
class ChatRoom(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    users = models.ManyToManyField(UserProfile)

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content_text = models.TextField(max_length = 300)
    send_date = models.DateTimeField('date_sended', auto_now_add=True)
