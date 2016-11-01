from django.shortcuts import redirect
from django.views import generic
from django.http import HttpResponse
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

def message_set(request, pk ):
    if request.method == "GET":
        if request.is_ajax():
            current_video = Video.objects.get(pk=pk)
            data = Message.objects.filter(chat_room = current_video.chatroom).order_by('send_date')
            top = data.count()
            bot = top - 50
            data = data[bot:top]
            data_txt = ""
            for sms in data:
                data_txt += "<p>" + sms.author.user.username + ": " + sms.content_text + "</p>"
            return HttpResponse(data_txt)
