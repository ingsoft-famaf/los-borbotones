from __future__ import unicode_literals

from django.db import models

from videos.models import Video
from users.models import UserProfile

# Create your models here.
class ChatRoom(models.Model):
    video = models.OneToOneField(
        Video,
        on_delete=models.CASCADE,
        )



class Message(models.Model):
    chat_room = models.ForeignKey(
        ChatRoom,
        null=True
        #on_delete=models.SET_DEFAULT,
        )
    author = models.ForeignKey(
        UserProfile,
        null=True
        #on_delete=models.SET_DEFAULT,
    )
    content_text = models.TextField(max_length = 300)
    send_date = models.DateTimeField('date_sended', auto_now_add=True)