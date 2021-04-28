from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserCreationForm, MyUserChangeForm
from .models import User, Venue, Post, CheckIn

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = User
    list_display = [
        'username', #dev only
        'city',
        'state', 
        'bio_text',  
        'prof_pic', 
        'prof_pic_img',
        'star_user',  
    ]
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': (    
            'city',
            'state', 
            'bio_text',  
            'prof_pic', 
            'prof_pic_img',
            'star_user',  
            'users_following_list', 
            'venues_following_list')}),
    ) #this will allow to change these fields in admin module



admin.site.register(User, MyUserAdmin)
admin.site.register(Venue)
admin.site.register(Post)
admin.site.register(CheckIn)

