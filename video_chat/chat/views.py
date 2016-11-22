from django.shortcuts import redirect
from django.views import generic
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from models import ChatRoom, Message
from users.models import UserProfile
from videos.models import Video
from forms import MessageForm
# Create your views here.
@login_required()
def create_message(request):
    if request.method == 'POST':
        if request.is_ajax():
            new_message_form = MessageForm(request.POST)
            if new_message_form.is_valid():
                new_message = new_message_form.save(commit=False)
                new_message.author = UserProfile.objects.get(pk=request.user.userprofile.pk)
                new_message.chat_room = ChatRoom.objects.get(pk=request.POST['chat_id'])
                new_message.save()
                return JsonResponse(request.POST)
            else:
                return redirect("/")
        else:
            return redirect("/")
    else:
        return redirect("/")
        
@login_required()
def message_set(request, pk ):
    if request.method == "GET":
        if request.is_ajax():
            chatroom = ChatRoom.objects.get(pk = pk)
            data = Message.objects.filter(chat_room = chatroom).order_by('send_date')
            top = data.count()
            if top-50 < 0:
                bot = 0
            else:
                bot = top-50
            data = data[bot:top]
            data_txt = ""
            for sms in data:
                data_txt += "<p>" + sms.author.user.username + ": " + sms.content_text + "</p>"
            return HttpResponse(data_txt)
