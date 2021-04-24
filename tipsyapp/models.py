from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True, null=True)
    twitter_handle= models.CharField(max_length= 15, blank=True, null=True)
    insta_handle= models.CharField(max_length= 30, blank=True, null=True)
    fb_link = models.URLField(max_length=160, blank=True, null= True)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    bio_text = models.TextField(max_length=500, blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    prof_pic = models.URLField(max_length=300)
    star_user = models.BooleanField(default=False)
    users_following_list = models.ManyToManyField('User', related_name="user_follows", blank=True)
    users_followed_by_list = models.ManyToManyField('User', related_name="followed_by", blank=True)
    venues_following_list = models.ManyToManyField('Venue', related_name="venue_follows", blank=True)
    posts_liked = models.ManyToManyField('Post', related_name="posts_liked", blank = True)

    class Meta:
        ordering=['join_date']

    def __str__(self):
        return f'{self.username}'



VENUE_TYPE = [
    ('brewery', 'Brewery'),
    ('distillery', 'Distillery'),
    ('winery', 'Winery'),
]


TAG_LIST = [
    ('1', 'Outside Seating/Patio'),
    ('2', 'Pet Friendly'),
    ('3', 'Great Appetizers'),
    ('4', 'Large Variety of Draft Beers'),
]

class Venue(models.Model):
    BREWERY = "brewery"
    DISTILLERY = 'distillery'
    WINERY = 'winery'
    
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
    venue_type = models.CharField(choices=BDW_CHOICES, default='brewery', max_length=30)
    venue_added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="venue_added_by")
    is_authenticated = models.BooleanField(default=False)
    hours_of_operation = models.TextField(max_length=300)
    web_url = models.URLField(max_length=200)
    email = models.EmailField(max_length=254)
    twitter_handle= models.CharField(max_length= 15, blank=True, null=True)
    insta_handle= models.CharField(max_length= 30, blank=True, null=True)
    fb_link = models.URLField(max_length=160, blank=True, null=True)
    phone_num = models.CharField(max_length=12, blank=True, null=True )
    street_address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    zip = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    prof_pic = models.URLField(max_length=300, blank=True, null=True)
    followers_list = models.ManyToManyField('User', related_name="venue_followers", blank=True)
    tags = models.CharField(choices=TAG_CHOICES, blank=True, null=True, max_length=103)
    join_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=['join_date']

    def __str__(self):
        return f'{self.venue_name}'


class Post(models.Model):
    post_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, unique=True)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts_by")
    posted_to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_to_user", blank=True, null=True)
    posted_to_venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="posted_to_venue", blank=True, null=True)
    post_likers = models.ManyToManyField('User', related_name="post_likers", blank = True)
    post_date = models.DateTimeField(auto_now_add=True)
    post_img = models.URLField(max_length=300, blank=True, null=True)
    post_text = models.TextField(max_length=800, blank=True, null=True)  

    class Meta:
        ordering=['post_date']
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_post_on_user_OR_venue",
                check=(
                    models.Q(
                        posted_to_user__isnull=False,
                        posted_to_venue__isnull=True,
                    )
                    | models.Q(
                        posted_to_user__isnull=True,
                        posted_to_venue__isnull=False,
                    )
                ),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_post_text_ANDOR_img",
                check=(
                    models.Q(
                        post_img__isnull=False,
                        post_text__isnull=False,
                    )
                    | models.Q(
                        post_img__isnull=True,
                        post_text__isnull=False,
                    )
                    | models.Q(
                        post_img__isnull=False,
                        post_text__isnull=True,
                    )
                ),
            )            
        ]        

    def __str__(self):
        return f'{self.post_id}'    

