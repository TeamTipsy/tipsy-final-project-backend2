from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserCreationForm, MyUserChangeForm
from .models import User, Venue, Post

class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    model = User
    list_display = [
        'city',
        'state', 
        'bio_text',  
        'prof_pic', 
        'star_user',  
        'users_following_num', 
        'venues_following_num', 
    ]
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': (
            'city',
            'state', 
            'bio_text',  
            'prof_pic', 
            'star_user',  
            'users_following_num', 
            'venues_following_num')}),
    ) #this will allow to change these fields in admin module



admin.site.register(User, MyUserAdmin)
admin.site.register(Venue)
admin.site.register(Post)
