from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
import uuid
from multiselectfield import MultiSelectField

def user_directory_path(instance, filename):
    return 'profile/{0}/{1}'.format(instance.user_id, filename)

def venue_directory_path(instance, filename):
    return 'venue/{0}/{1}'.format(instance.venue_id, filename)
 
def post_directory_path(instance, filename):
    return 'post/{0}/{1}'.format(instance.post_id, filename)


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True, null=True)
    twitter_handle = models.CharField(max_length= 15, blank=True, null=True)
    insta_handle = models.CharField(max_length= 30, blank=True, null=True)
    fb_link = models.URLField(max_length=160, blank=True, null= True)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    bio_text = models.TextField(max_length=500, blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    prof_pic = models.ImageField(null=True, blank=True, upload_to=user_directory_path)
    prof_pic_url = models.URLField(null=True, blank=True, max_length=400)
    banner_img = models.ImageField(null=True, blank=True, upload_to=user_directory_path)
    banner_img_url = models.URLField(null=True, blank=True, max_length=400)
    star_user = models.BooleanField(default=False)
    is_private = models.BooleanField(null=True, blank=True)
    users_following_list = models.ManyToManyField('User', related_name="user_follows", blank=True)
    users_followed_by_list = models.ManyToManyField('User', related_name="followed_by", blank=True)
    venues_following_list = models.ManyToManyField('Venue', related_name="venue_follows", blank=True)
    posts_liked = models.ManyToManyField('Post', related_name="posts_liked", blank = True)

    class Meta:
        ordering=['-join_date']

    def __str__(self):
        return f'{self.username}'

# This fixes a bug where users without prof pics were breaking post author serializer
    @property
    def pp_url(self):
        if self.prof_pic and hasattr(self.prof_pic, 'url'):
            return self.prof_pic.url
        # return 'null'



VENUE_TYPE = [
    ('brewery', 'Brewery'),
    ('distillery', 'Distillery'),
    ('winery', 'Winery'),
]


TAG_LIST = [
    ('Outdoor Seating/Patio', 'Outdoor Seating/Patio'),
    ('Pet Friendly', 'Pet Friendly'),
    ('Appetizers', 'Appetizers'),
    ('Large Variety of Draft Beers', 'Large Variety of Draft Beers'),
    ('Cider Options', 'Cider Options'),
    ('Wine Options', 'Wine Options'),
    ('Trivia', 'Trivia'),
    ('Live Entertainment', 'Live Entertainment'),
    ('Knowledgable Staff', 'Knowledgable Staff'),
    ('Flea Markets', 'Flea Markets'),
    ('Beer Options', 'Beer Options'),
    ('Food Trucks', 'Food Trucks'),
    ('MUST VISIT!', 'MUST VISIT!'),
    ('Friendly Staff', 'Friendly Staff'),
    ('Indoor Seating', 'Indoor Seating'),
    ('Cool Vibes', 'Cool Vibes'),
    ('Hazy IPAs', 'Hazy IPAs'),
    ('NE IPAs', 'NE IPAs'),
    ('Sours/Goses', 'Sours/Goses'),
    ('Saisons', 'Saisons'),
    ('Lagers', 'Lagers'),
    ('Amber/Red Ales', 'Amber/Red Ales'),
    # ('23', ''),
    # ('24', ''),
    # ('25', ''),
    # ('26', ''),
    # ('27', ''),
    # ('28', ''),
    # ('29', ''),
    # ('30', ''),
    # ('31', ''),
    # ('32', ''),
    # ('33', ''),
    # ('34', ''),
    # ('35', ''),
    # ('36', ''),
]


class Venue(models.Model):
    BREWERY = "Brewery"
    DISTILLERY = 'Distillery'
    WINERY = 'Winery'
    
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
    v_prof_pic = models.ImageField(blank=True, null=True, upload_to=venue_directory_path)
    v_prof_pic_url = models.URLField(null=True, blank=True, max_length=400)
    v_banner_img = models.ImageField(blank=True, null=True, upload_to=venue_directory_path)
    v_banner_img_url = models.URLField(null=True, blank=True, max_length=400)
    venue_img_caption = models.CharField(blank=True, null=True, max_length=100)
    followers_list = models.ManyToManyField('User', related_name="venue_followers", blank=True)
    tags = MultiSelectField(choices=TAG_LIST, blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=['-join_date']

    def __str__(self):
        return f'{self.venue_name}'



class Post(models.Model):
    post_id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, unique=True)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts_by")
    posted_to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_to_user", blank=True, null=True)
    posted_to_venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="posted_to_venue", blank=True, null=True)
    post_likers = models.ManyToManyField('User', related_name="post_likers", blank = True)
    post_date = models.DateTimeField(auto_now_add=True)
    post_img_1 = models.ImageField(null=True, blank=True, upload_to=post_directory_path)
    post_img_url = models.URLField(null=True, blank=True, max_length=400)
    # post_img_2 = models.ImageField(null=True, blank=True, upload_to=post_directory_path)
    # post_img_3 = models.ImageField(null=True, blank=True, upload_to=post_directory_path)
    post_text = models.TextField(max_length=800, blank=True, null=True)  


    class Meta:
        ordering=['-post_date']
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
                        post_img_1__isnull=False,
                        post_text__isnull=False,
                    )
                    | models.Q(
                        post_img_1__isnull=True,
                        post_text__isnull=False,
                    )
                    | models.Q(
                        post_img_1__isnull=False,
                        post_text__isnull=True,
                    )
                ),
            )            
        ]        

    def __str__(self):
        return f'{self.post_id}'    

class CheckIn(models.Model):
    checkin_user = models.ForeignKey(User, on_delete=models.CASCADE, 
        related_name="checkin_user")
    checkedin_venue = models.ForeignKey(Venue, on_delete=models.CASCADE, 
        related_name="checkedin_venue")
    checkin_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-checkin_time']

    def __str__(self):
        return f'check in at venue {self.checkedin_venue} user at {self.checkin_time}'


