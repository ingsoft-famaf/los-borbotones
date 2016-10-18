from django.conf.urls import url
from . import views

app_name = 'videos'
urlpatterns = [
    url(r'^search/(?P<search_key>[\w\-]+)/$', views.SearchView.as_view(), name='search'),
    url(r'^home/$', views.Home.as_view(), name='search'),

    #url(r'^(?P<video_id>[0-9]+)/delete/$', views.delete, name='delete'),
]
