from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Venue, Post

class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = (
            'city',
            'state', 
            'bio_text',  
            # 'prof_pic', 
            # 'banner_img',
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
            # 'prof_pic', 
            'star_user',  
            'users_following_list', 
            )


# class Upload(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = (
#             'prof_pic_img',
#         )


# class VenueUpload(forms.ModelForm):

#     class Meta:
#         model = Venue
#         fields = (
#             'venue_img',
#             'venue_img_caption',
#         )


# class PostUpload(forms.ModelForm):

#     class Meta:
#         model = Post
#         fields = (
#             'post_img_file',
#             'post_img_caption',
#         )