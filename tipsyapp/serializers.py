from rest_framework import serializers
from .models import User, Venue

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',    
            'last_name',
            'email',    
            'city',
            'state', 
            'bio_text',  
            'prof_pic', 
            'star_user',  
            'users_following_num', 
            # 'users_following_list', 
            'venues_following_num', 
            'venues_following_list', 
        ]


class VenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue
        fields = [
            'venue_name',
            'venue_type',
            'is_authenticated',
            'hours_of_operation',
            'web_url',
            'email',
            'street_address',
            'city',
            'state',
            'prof_pic',
            'followers_num',
            'tags', 
        ]
