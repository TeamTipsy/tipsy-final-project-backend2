from django.db import models
from django.contrib.auth.models import AbstractUser
from annoying.fields import AutoOneToOneField
import uuid

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, unique=True)  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    bio_text = models.TextField(max_length=500, blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    prof_pic = models.URLField(max_length=300)
    star_user = models.BooleanField(default=False)
    users_following_num = models.IntegerField(default=0)
    users_following_list = models.ManyToManyField('User', related_name="user_follows", blank=True)
    users_followed_by_list = models.ManyToManyField('User', related_name="followed_by", blank=True)
    venues_following_num = models.IntegerField(default=0)
    venues_following_list = models.ManyToManyField('Venue', related_name="venue_follows", blank=True)

    class Meta:
        ordering=['join_date']

    def __str__(self):
        return f'{self.first_name}'

# class UserProfile(models.Model):
#     user = AutoOneToOneField(User, on_delete=models.CASCADE)
#     follows = models.ManyToManyField('UserProfile', related_name="followed_by", blank=True)

#     def __str__(self):
#         return f'{self.first_name}'


VENUE_TYPE = [
    ('br', 'Brewery'),
    ('ds', 'Distillery'),
    ('wn', 'Winery'),
]


TAG_LIST = [
    ('1', 'Outside Seating/Patio'),
    ('2', 'Pet Friendly'),
    ('3', 'Great Appetizers'),
    ('4', 'Large Variety of Draft Beers'),
]

class Venue(models.Model):
    BREWERY = "br"
    DISTILLERY = 'ds'
    WINERY = 'wn'
    
    BDW_CHOICES = [
        (BREWERY, 'Brewery'),
        (DISTILLERY, 'Distillery'),
        (WINERY, 'Winery'),
    ]

    OUTSIDE_SEATING = "1"
    PET_FRIENDLY = "2"
    APPETIZERS = "3"
    LOTSODRAFTS = "4"

    TAG_CHOICES = [
        (OUTSIDE_SEATING, 'Outside Seating/Patio'),
        (PET_FRIENDLY, 'Pet Friendly'),
        (APPETIZERS, 'Great Appetizers'),
        (LOTSODRAFTS, 'Large Variety of Draft Beers'),
    ]

    venue_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, unique=True) 
    venue_name = models.CharField(max_length=100)
    venue_type = models.CharField(choices=BDW_CHOICES, default='br', max_length=30)
    is_authenticated = models.BooleanField(default=False)
    hours_of_operation = models.TextField(max_length=300)
    web_url = models.URLField(max_length=200)
    email = models.EmailField(max_length=254)
    street_address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    prof_pic = models.URLField(max_length=300)
    followers_num = models.IntegerField(default=0)
    followers_list = models.ManyToManyField(User, related_name="venue_followers", blank=True)
    # comments = models.ManyToManyField()
    tags = models.CharField(choices=TAG_CHOICES, blank=True, null=True, max_length=103)
    # menu_images = models.ManyToManyField()
    # user_uploaded_images = models.ManyToManyField()


    join_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=['join_date']

    def __str__(self):
        return f'{self.venue_name}'


class Post(models.Model):
    post_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, unique=True) 
    post_author = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_to = models.ForeignKey(Venue, on_delete=models.CASCADE)
    post_img = models.URLField(max_length=300, blank=True)
    post_text = models.TextField(max_length=800, blank=True, null=True)  
    post_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['post_date']

    def __str__(self):
        return self.post_id    