from rest_framework import serializers, fields
from .models import CheckIn, User, Venue, Post, CheckIn


class PostSerializer(serializers.ModelSerializer):
    # post_author = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    #     )
    post_author_username = serializers.ReadOnlyField(source='post_author.username')
    post_author_id = serializers.ReadOnlyField(source='post_author.user_id')
    post_author_pic = serializers.ReadOnlyField(source='post_author.prof_pic')
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
            'post_img',
            'post_text',
        ]        


class CheckInSerializer(serializers.ModelSerializer):
    checkin_user_id = serializers.ReadOnlyField(source='checkin_user.user_id')
    checkin_username = serializers.ReadOnlyField(source='checkin_user.username')
    # checkedin_venuename = checkedin_venue
   
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

    # checked_in_at = CheckInSerializer(
    #     many=True, read_only=True
    #     )    
    checkin_user = CheckInSerializer(
        many=True, read_only=True
        )    
    # posts_by = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Post.objects.all()
    #     ) # Leaving this here in case we want it- this renders pk of posts instead of posts themselves
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
            'users_following_list', 
            'users_followed_by_list', 
            'venues_following_list', 
            'posts_liked',
            'posts_by',
            'posted_to_user',
            'checkin_user',
        ]


class VenueSerializer(serializers.ModelSerializer):
    # venue_info = VenueInfoSerializer(source='*', read_only=True)

    checkedin_venue = CheckInSerializer(
        many=True, read_only=True
        )
    # checkins = CheckInSerializer(
    #     many=True, read_only=True
    #     )

    posted_to_venue = PostSerializer(
        many=True, read_only=True
        )
    # posted_to_venue = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Post.objects.all()
    #     ) # see comment for same code under userserializer
    venue_added_by = serializers.ReadOnlyField(source='venue_added_by.username')
        
        
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
            'prof_pic',
            'followers_list',
            'tags', 
            'join_date',
            'posted_to_venue',
            'checkedin_venue',
        ]


