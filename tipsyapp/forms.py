from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = (
            'city',
            'state', 
            'bio_text',  
            'prof_pic', 
            'star_user',  
            'users_following_list',
            )

class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = (
            'city',
            'state', 
            'bio_text',  
            'prof_pic', 
            'star_user',  
            'users_following_list', 
            )


class Upload(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'prof_pic_img',
        )