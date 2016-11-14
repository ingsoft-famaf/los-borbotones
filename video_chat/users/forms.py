from users.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        if User.objects.filter(Q(email = email) | Q(username = email)).exclude(username = username).count():
            raise forms.ValidationError(u'La direccion email ya esta siendo utilizada')
        return email

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
