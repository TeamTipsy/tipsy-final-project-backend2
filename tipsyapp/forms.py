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
            'users_following_num', 
            'users_following_list',
            'venues_following_num' 
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
            'users_following_num', 
            'venues_following_num'
            )