from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'users'
urlpatterns = [
    #url(r'^(?P<video_id>[0-9]+)/delete/$', views.delete, name='delete'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
