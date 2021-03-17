from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __str__(self):
        return f'{self.user.username} Profile'


class ImageUploadForm(forms.Form):
    profile_photo = forms.ImageField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']


