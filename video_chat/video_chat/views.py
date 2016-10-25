from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView
from django.urls import reverse
from django.http import Http404


class RedirectSearch(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        search = self.request.GET['search']
        search_key = self.request.GET['search_key']

        if (search == 'usuarios'):
            url = reverse('users:search') + "?search_key=" + search_key
        elif (search == 'videos'):
            url = reverse('videos:search') + "?search_key=" + search_key
        else:
            raise Http404

        return url 