from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'videos'
urlpatterns = [
    url(r'^search/$', views.SearchVideo.as_view(), name='search'),
    url(r'^play/(?P<pk>\d+)/$', views.Play.as_view(), name='play'), #TODO
    url(r'^upload/$', views.Upload.as_view(), name='upload'),
	url(r'^(?P<pk>\d+)/delete/$', views.Delete.as_view(), name='delete'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
