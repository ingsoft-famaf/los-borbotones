# -*- coding: utf-8 -*-
from users.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'class': 'form-control',
            'type': 'text',
            'name': 'username',
            'id': 'username',
            'tabindex': '1',
            'placeholder': 'Usuario'
        }
        self.fields['email'].widget.attrs = {
            'class': 'form-control',
            'type': 'text',
            'name': 'email',
            'id': 'email',
            'tabindex': '1',
            'placeholder': 'Correo electrónico'
        }
        self.fields['password'].widget.attrs = {
            'class': 'form-control',
            'type': 'password',
            'name': 'password',
            'id': 'password',
            'tabindex': '2',
            'placeholder': 'Contraseña'
        }

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
