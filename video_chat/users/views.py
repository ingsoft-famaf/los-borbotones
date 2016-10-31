from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
import datetime

from .loginmailorusername import authenticatemailoruser
from videos.models import Video

# Create your views here.

from users.forms import UserForm, UserProfileForm
from users.models import UserProfile


def Register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

            return redirect('home')

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
            'users/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def UserLogin(request):
    context = RequestContext(request)

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticatemailoruser(self=request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('home')#TODO Login_redirect / next
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return render(request, 'users/login.html', {'error_message': "The user or password is incorrect"})
    else:

        return render(request, 'users/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


class UserProfileDetail(LoginRequiredMixin, generic.DetailView):
    template_name = "users/profile.html"
    model = UserProfile
    context_object_name = "userprofile"

    def get_context_data(self, **kwargs):
        data = super(UserProfileDetail,self).get_context_data(**kwargs)
        profile_pk = self.kwargs['pk']
        current_profile = UserProfile.objects.get(pk=profile_pk)
        data['video_list'] = current_profile.user.video_set.all()
        data['profile_pk'] = int(profile_pk)
        data['friends_list'] = current_profile.friend.all()
        return data


class SearchUser(LoginRequiredMixin, generic.ListView):
    template_name = 'users/search.html'
    context_object_name = 'founded_users'

    def get_queryset(self):
        key = self.request.GET['search_key']
        return(UserProfile.objects.filter(user__username__icontains = key))

@login_required
class AddFriend(generic.View):

    template_name = 'users/search.html'

    def get_queryset(self):
        friend = self.request.GET['key']
        UserProfile.user.friend.add(friend)

@login_required
class RemoveFriend(generic.View):

    template_name = 'users/remove_friends.html'

    def get_queryset(self):
        friend = self.request.GET['key']
        UserProfile.user.friend.remove(friend)