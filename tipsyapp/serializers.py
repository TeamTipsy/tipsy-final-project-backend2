from rest_framework import serializers, fields
from .models import User, Venue, Post, VenuePost


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
            'posts_liked',
            'venue_posts_liked',
        ]


class VenueAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = [
            'street_address',
            'city',
            'state',
            'zip',
        ]


class VenueInfoSerializer(serializers.ModelSerializer):
    venue_address = VenueAddressSerializer(source='*', read_only=True)
    
    class Meta:
        model = Venue
        fields = [
            'phone_num',
            'hours_of_operation',
            'web_url',
            'email',
            'twitter_handle',    
            'insta_handle',    
            'fb_link', 
            'venue_address', 
        ]


class VenueSerializer(serializers.ModelSerializer):
    venue_info = VenueInfoSerializer(source='*', read_only=True)
    class Meta:
        model = Venue
        fields = [
            'venue_id',
            'venue_name',
            'venue_type',
            'venue_info',
            'is_authenticated',
            'phone_num',
            'prof_pic',
            'followers_num',
            'followers_list',
            'tags', 
            'join_date',
        ]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'post_id',
            'post_author',
            'posted_to_user',
            'post_likers',
            'post_date',
            'post_img',
            'post_text',
        ]        

class VenuePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = VenuePost
        fields = [
            'venue_post_id',
            'venue_post_author',
            'posted_to_venue',
            'venue_post_likers',
            'venue_post_date',
            'venue_post_img',
            'venue_post_text',
        ]               