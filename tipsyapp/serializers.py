from rest_framework import serializers
from .models import User, Venue

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'first_name',    
            'last_name',
            'email',
            'twitter_handle',    
            'insta_handle',    
            'fb_link',    
            'city',
            'state', 
            'bio_text',  
            'prof_pic', 
            'join_date',
            'star_user',  
            'users_following_num', 
            'users_following_list', 
            'users_followed_by_list', 
            'venues_following_num', 
            'venues_following_list', 
        ]


class VenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue
        fields = [
            'venue_id',
            'venue_name',
            'venue_type',
            'is_authenticated',
            'hours_of_operation',
            'web_url',
            'email',
            'twitter_handle',    
            'insta_handle',    
            'fb_link', 
            'phone_num',
            'street_address',
            'city',
            'state',
            'zip',
            'prof_pic',
            'followers_num',
            'followers_list',
            'tags', 
            'join_date',
        ]
