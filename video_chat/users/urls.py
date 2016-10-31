from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.core.urlresolvers import reverse
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^search/$', views.SearchUser.as_view(), name='search'),
    url(r'^send/$', views.SendRequest, name='send_request')
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
