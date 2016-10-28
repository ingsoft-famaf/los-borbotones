from django.shortcuts import render
from django.views import generic

from models import ChatRoom
# Create your views here.
class ChatView(generic.DetailView):
    template_name = 'chat/chat.html'
    model = ChatRoom
    context_object_name = 'chatroom'

    def get_context_data(self, **kwargs):
        data = super(ChatView,self).get_context_data(**kwargs)
        data['message_list'] = ChatRoom.message_set.all()
        return data
class CreateMessage(generic.CreateView):
    
