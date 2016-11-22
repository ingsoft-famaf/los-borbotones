from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import Video
from .forms import UploadForm
from chat.models import ChatRoom


# Create your views here.
class SearchVideo(LoginRequiredMixin, generic.ListView):
    template_name = 'videos/search.html'
    context_object_name = 'founded_videos'

    def get_queryset(self):
        key = self.request.GET['search_key']
        return (Video.objects.filter(Q(title__icontains=key) | Q(description__icontains=key)).order_by('-pub_date'))


class Play(LoginRequiredMixin, generic.DetailView):
    template_name = 'videos/play.html'
    model = Video

    def get_context_data(self, **kwargs):
        data = super(Play, self).get_context_data(**kwargs)
        userprofile = self.request.user.userprofile
        chat = self.kwargs.get('chat')
        if (chat == None):
            chatroom = userprofile.chatroom_set.create(video=self.object)
        else:
            try:
                chatroom = ChatRoom.objects.get(pk=chat, video=self.object)
                if (userprofile not in chatroom.users.all()):
                    if ((chatroom.users.all() & userprofile.friends.all()).exists()):
                        chatroom.users.add(userprofile)
                    else: raise ObjectDoesNotExist
            except ObjectDoesNotExist:
                chatroom = userprofile.chatroom_set.create(video=self.object)

        data['chatroom'] = chatroom
        return data


class Upload(LoginRequiredMixin, generic.CreateView):
    model = Video
    form_class = UploadForm
    template_name = 'videos/upload.html'

    def get_success_url(self):
	chatroom = ChatRoom(video=self.object)
	chatroom.save()
        return reverse('profile', args = [self.request.user.id])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(Upload, self).form_valid(form)


class Delete(LoginRequiredMixin, generic.DeleteView):
    model = Video
    template_name = 'videos/delete_video.html'

    def get_object(self, **kwargs):
        video = super(generic.DeleteView, self).get_object()
        if not video.author == self.request.user:
            raise Http404
        return video

    def get_success_url(self):
        return reverse('profile', args = [self.request.user.id])