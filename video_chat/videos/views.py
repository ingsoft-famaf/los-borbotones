from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse

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

    def get_object(self):
        video = super(generic.DetailView, self).get_object()
        video.userprofile_set.add(self.request.user.userprofile)
        return video


class Upload(LoginRequiredMixin, generic.CreateView):
    model = Video
    form_class = UploadForm
    template_name = 'videos/upload.html'

    def get_success_url(self):
	chatroom = ChatRoom(video=self.object)
	chatroom.save()
        return reverse('profile', args = [self.request.user.id])

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super(Upload, self).form_valid(form)


class Delete(LoginRequiredMixin, generic.DeleteView):
    model = Video
    template_name = 'videos/delete_video.html'

    def get_object(self, **kwargs):
        video = super(generic.DeleteView, self).get_object()
        if not video.autor == self.request.user:
            raise Http404
        return video

    def get_success_url(self):
        return reverse('profile', args = [self.request.user.id])