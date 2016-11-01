from django.http import Http404
from videos.views import SearchVideo
from django.contrib.auth.decorators import login_required
from users.views import SearchUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


@login_required
def RedirectSearch(request):
    search = request.GET['search']
    search_key = request.GET['search_key']

    if (search == 'users'):
        return SearchUser.as_view()(request)
    elif (search == 'videos'):
        return SearchVideo.as_view()(request)
    else:
        raise Http404

class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'video_chat/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['friends_list'] = self.request.user.userprofile.friend.all()
        return context