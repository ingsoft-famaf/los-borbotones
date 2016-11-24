# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.db.models import Q

from .loginmailorusername import authenticatemailoruser
from videos.models import Video

# Create your views here.

from users.forms import UserForm, UserProfileForm
from users.models import UserProfile, FriendRequest


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
            login(request, user)
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
            return render(request, 'users/register.html', {'error_message': "El usuario o contraseña son incorrectos", 'user_form': UserForm(), 'profile_form': UserProfileForm()})
    else:
        return render(request, 'users/register.html', {'user_form': UserForm(), 'profile_form': UserProfileForm()})


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
        user = self.request.user
        profile_pk = self.kwargs['pk']
        current_profile = UserProfile.objects.get(pk=profile_pk)
        data['video_list'] = current_profile.user.video_set.all()
        data['profile_pk'] = int(profile_pk)

        if ((current_profile.pk != user.pk) and (not
            FriendRequest.objects.filter(Q(sender=user, receiver=current_profile.user) |
                Q(sender=current_profile.user, receiver=user)).exists())):
            data['can_send'] = True
        else:
            data['can_send'] = False

        if current_profile in user.userprofile.friends.all():
            data['is_friend'] = True
        else:
            data['is_friend'] = False
            
        return data


class SearchUser(LoginRequiredMixin, generic.ListView):
    template_name = 'users/search.html'
    context_object_name = 'founded_users'

    def get_queryset(self):
        key = self.request.GET['search_key']
        return(UserProfile.objects.filter(user__username__icontains = key).exclude(pk = self.request.user.userprofile.pk))

@login_required
def SendRequest(request):
    user = request.user
    if request.method == 'POST':
        friend_pk = request.POST['friend_pk']
        friend = User.objects.get(pk=friend_pk)
        if ((not FriendRequest.objects.filter(sender=friend, receiver=user).exists()) 
            and (not user.userprofile.friends.filter(pk=friend_pk).exists())):
            FriendRequest.objects.get_or_create(sender=user, receiver=friend)
    return redirect('home')

@login_required
def AcceptRequest(request):
    userprofile = request.user.userprofile
    if request.method == 'POST':
        friend_pk = request.POST['friend_pk']
        friend = UserProfile.objects.get(pk=friend_pk)

        qs = FriendRequest.objects.filter(sender=friend.user, receiver=userprofile.user)
        if qs.exists():
            qs.delete()
            if not userprofile.friends.filter(pk=friend_pk).exists():
                userprofile.friends.add(friend)
    return redirect('users:requests')

@login_required
def DeleteRequest(request):
    if request.method == 'POST' :
        friend_request = FriendRequest.objects.get(pk = request.POST['friend_request'])
        if friend_request.receiver == request.user :
            friend_request.delete()
    return redirect('users:requests')

@login_required
def RemoveFriend(request):
    userprofile = request.user.userprofile
    if request.method == 'POST':
        friend_pk = request.POST['friend_pk']
        friend = UserProfile.objects.get(pk=friend_pk)
        userprofile.friends.remove(friend)
    return redirect('home')

class ViewRequests(LoginRequiredMixin, generic.ListView):
    model = FriendRequest
    template_name = 'users/requests.html'
    context_object_name = 'requests_list'

    def get_queryset(self):
        return(self.request.user.receiver.all())

class ViewFriends(LoginRequiredMixin, generic.ListView):
    model = UserProfile
    template_name = 'users/friends_list.html'
    context_object_name = 'friends_list'

    def get_queryset(self):
        return(self.request.user.userprofile.friends.all())