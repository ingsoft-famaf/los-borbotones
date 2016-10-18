from django.shortcuts import render
from django.views import generic

from .models import Video

# Create your views here.
class SearchView(generic.ListView):
    template_name = 'videos/search.html'
    context_object_name = 'founded_videos'

    def get_queryset(self):
        """Return the last five published questions."""
        return Video.objects.filter(title__contains=self.kwargs['search_key'])