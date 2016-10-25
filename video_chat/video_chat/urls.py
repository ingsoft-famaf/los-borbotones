"""video_chat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from video_chat import views as project_views
from videos import views as videos_views
from users import views as users_views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^search/$', project_views.RedirectSearch.as_view(), name='redirect_search'),
    url(r'^video/', include('videos.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^$', videos_views.Home.as_view(), name='home'),
    url(r'^register/$', users_views.Register, name='register'),
    url(r'^login/$', users_views.UserLogin, name='login'),
    url(r'^logout/$', users_views.user_logout, name='logout'),
    url(r'^profile/(?P<pk>\d+)/$', users_views.UserProfileDetail.as_view(), name='profile'),
    url(r'^admin/', admin.site.urls),
]
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
