from django.conf.urls import url
from . import views

app_name = 'videos'
urlpatterns = [
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^play/(?P<pk>\d+)/$', views.Play.as_view(), name='play'), #TODO

    #url(r'^(?P<video_id>[0-9]+)/delete/$', views.delete, name='delete'),
]
