from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.core.urlresolvers import reverse
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^search/$', views.SearchUser.as_view(), name='search'),
    url(r'^send/$', views.SendRequest, name='send_request'),
    url(r'^requests/$', views.ViewRequests.as_view(), name='requests'),
    url(r'^accept/$', views.AcceptRequest, name='accept_request'),
    url(r'^decline/$', views.DeleteRequest, name='decline_request'),
    url(r'^delete/$', views.RemoveFriend, name='delete_friend'),
    url(r'^friends/$', views.ViewFriends.as_view(), name='friends'),
    url(r'^last_video/$', views.last_video, name='last_video'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
