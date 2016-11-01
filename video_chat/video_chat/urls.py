from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from video_chat import views as project_views
from videos import views as videos_views
from users import views as users_views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^search/$', project_views.RedirectSearch, name='redirect_search'),
    url(r'^video/', include('videos.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^$', project_views.Home.as_view(), name='home'),
    url(r'^chat/', include('chat.urls')),
    url(r'^register/$', users_views.Register, name='register'),
    url(r'^login/$', users_views.UserLogin, name='login'),
    url(r'^logout/$', users_views.user_logout, name='logout'),
    url(r'^profile/(?P<pk>\d+)/$', users_views.UserProfileDetail.as_view(), name='profile'),
    url(r'^admin/', admin.site.urls),
]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
