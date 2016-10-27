from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse

from .models import Video
from .forms import VideoForm

# Create your views here.
class SearchVideo(LoginRequiredMixin, generic.ListView):
    template_name = 'videos/search.html'
    context_object_name = 'founded_videos'

    def get_queryset(self):
        key = self.request.GET['search_key']
        return (Video.objects.filter(Q(title__icontains=key) | Q(description__icontains=key)).order_by('-pub_date'))


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'video_chat/home.html'


class Play(LoginRequiredMixin, generic.DetailView):
    template_name = 'videos/play.html'
    model = Video
    # TODO ultimo video visto


def Upload(LoginRequiredMixin, request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.autor = request.user
            video.save()
            return HttpResponse('<script type="text/javascript">window.close();</script>')
    else:
        form = VideoForm()
    return render(request, 'videos/upload.html', {
        'form': form
    })


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
