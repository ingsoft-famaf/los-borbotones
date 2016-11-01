from django.conf.urls import url

from . import views
app_name = 'chat'

urlpatterns = [
    url(r'chat/$', views.create_message, name='chat'),
    url(r'messages/(?P<pk>\d+)$', views.message_set, name='message_set')
    ]
