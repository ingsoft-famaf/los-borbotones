from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Video
from .forms import VideoForm

# Create your views here.
class SearchView(LoginRequiredMixin, generic.ListView):
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

@login_required()
def Upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.autor = request.user
            video.save()
            return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'videos/upload.html', {
        'form': form
    })
