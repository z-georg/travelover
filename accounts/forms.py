from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from accounts.models import UserProfileInfo


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileInfoFrom(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        exclude = ('user',)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(), )
