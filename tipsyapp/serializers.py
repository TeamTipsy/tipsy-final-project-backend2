from rest_framework import serializers, fields
from .models import User, Venue, Post
from .models import TAG_LIST


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


class UserSerializer(serializers.ModelSerializer):
    posts_by = PostSerializer(
        many=True, read_only=True
        )
    posted_to_user = PostSerializer(
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
        ]


# class VenueAddressSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Venue
#         fields = [
#             'street_address',
#             'city',
#             'state',
#             'zip',
#         ]


# class VenueInfoSerializer(serializers.ModelSerializer):
#     venue_address = VenueAddressSerializer(source='*', read_only=True)
    
#     class Meta:
#         model = Venue
#         fields = [
#             'phone_num',
#             'hours_of_operation',
#             'web_url',
#             'email',
#             'twitter_handle',    
#             'insta_handle',    
#             'fb_link', 
#             'venue_address', 
#         ]           


class VenueSerializer(serializers.ModelSerializer):
    # venue_info = VenueInfoSerializer(source='*', read_only=True)
    posted_to_venue = PostSerializer(
        many=True, read_only=True
        )
    # posted_to_venue = serializers.PrimaryKeyRelatedField(
    #     many=True, queryset=Post.objects.all()
    #     ) # see comment for same code under userserializer
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
            'prof_pic',
            'followers_list',
            'tags', 
            'join_date',
            'posted_to_venue',
        ]


