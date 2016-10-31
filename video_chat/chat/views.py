from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse

from django.contrib.auth.mixins import LoginRequiredMixin

from models import ChatRoom, Message
from users.models import UserProfile
from videos.models import Video
from forms import MessageForm
# Create your views here.

def create_message(request):
    if request.method == 'POST':
        if request.is_ajax():
            new_message_form = MessageForm(request.POST)
            if new_message_form.is_valid():
                new_message = new_message_form.save()
                new_message.author = UserProfile.objects.get(pk=request.user.pk)
                new_message.chat_room = ChatRoom.objects.get(pk=request.POST['chat_id'])
                new_message.save()
                return JsonResponse(request.POST)
            else:
                return redirect("/")
        else:
            return redirect("/")
    else:
        return redirect("/")

def message_set(request):
    if request.method == "GET":
        if request.is_ajax():
            data['messages_in_chat'] = Message.objects.filter(chat_room = current_video.chatroom)
            return JsonResponse(data)
