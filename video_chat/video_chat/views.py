from django.http import Http404
from videos.views import SearchVideo
from django.contrib.auth.decorators import login_required
from users.views import SearchUser


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