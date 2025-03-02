from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserImage, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['image']

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']