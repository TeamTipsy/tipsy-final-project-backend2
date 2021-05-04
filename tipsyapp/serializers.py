from rest_framework import serializers, fields
from .models import User, Venue, Post, CheckIn
from .models import TAG_LIST



class PostSerializer(serializers.ModelSerializer):
    post_author_username = serializers.ReadOnlyField(source='post_author.username')
    post_author_id = serializers.ReadOnlyField(source='post_author.user_id')
    post_author_pic = serializers.ReadOnlyField(source='post_author.pp_url')
    posted_to_venue_name = serializers.ReadOnlyField(source='posted_to_venue.venue_name')
    posted_to_username = serializers.ReadOnlyField(source='posted_to_user.username')

    class Meta:
        model = Post
        fields = [
            'post_id',
            'post_author_username',
            'post_author_id',
            'post_author_pic',
            'posted_to_user',
            'posted_to_username',
            'posted_to_venue',
            'posted_to_venue_name',
            'post_likers',
            'post_date',
            'post_img_1',
            'post_text',
        ]        


class CheckInSerializer(serializers.ModelSerializer):
    checkin_user_id = serializers.ReadOnlyField(source='checkin_user.user_id')
    checkin_username = serializers.ReadOnlyField(source='checkin_user.username')
   
    class Meta:
        model = CheckIn
        fields = [
            'checkin_user_id',
            'checkin_username',
            'checkedin_venue',
            'checkin_time',
        ]



class UserSerializer(serializers.ModelSerializer):
    posts_by = PostSerializer(
        many=True, read_only=True
        )
    posted_to_user = PostSerializer(
        many=True, read_only=True
        )

    checkin_user = CheckInSerializer(
        many=True, read_only=True
        )    

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
            # 'prof_pic_url', 
            'prof_pic', 
            # 'banner_img_url',
            'banner_img',
            'join_date',
            'star_user',  
            'users_following_list', 
            'users_followed_by_list', 
            'venues_following_list', 
            'posts_liked',
            'posts_by',
            'posted_to_user',
            'checkin_user',
        ]


class VenueSerializer(serializers.ModelSerializer):

    checkedin_venue = CheckInSerializer(
        many=True, read_only=True
        )

    posted_to_venue = PostSerializer(
        many=True, read_only=True
        )
    venue_added_by = serializers.ReadOnlyField(source='venue_added_by.username')
    tags = fields.MultipleChoiceField(choices=TAG_LIST)
        
        
    class Meta:
        model = Venue
        fields = [
            'venue_id',
            'venue_name',
            'venue_type',
            'phone_num',
            'hours_of_operation',
            'web_url',
            'email',
            'twitter_handle',    
            'insta_handle',    
            'fb_link', 
            'street_address',
            'city',
            'state',
            'zip',
            'venue_added_by',
            # 'venue_info',
            'is_authenticated',
            'v_prof_pic', 
            # 'v_prof_pic_url', 
            'v_banner_img',
            # 'v_banner_img_url',
            'followers_list',
            'tags', 
            'join_date',
            'posted_to_venue',
            'checkedin_venue',
        ]


