from django.shortcuts import render, redirect
from django.views import generic

from .models import Video
from .forms import VideoForm

# Create your views here.
class SearchView(generic.ListView):
    template_name = 'videos/search.html'
    context_object_name = 'founded_videos'

    def get_queryset(self):
        """Return the last five published questions."""
        return Video.objects.filter(title__icontains=self.request.GET['search_key'])

class Home(generic.TemplateView):
    template_name = 'video_chat/home.html'

class Play(generic.DetailView):
    template_name = 'videos/play.html'
    model = Video
    # TODO ultimo video visto

def Upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'videos/upload.html', {
        'form': form
    })
