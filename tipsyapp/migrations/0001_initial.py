# Generated by Django 3.2 on 2021-04-24 09:08

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=32, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('twitter_handle', models.CharField(blank=True, max_length=15, null=True)),
                ('insta_handle', models.CharField(blank=True, max_length=30, null=True)),
                ('fb_link', models.URLField(blank=True, max_length=160, null=True)),
                ('city', models.CharField(max_length=150)),
                ('state', models.CharField(max_length=150)),
                ('bio_text', models.TextField(blank=True, max_length=500, null=True)),
                ('join_date', models.DateTimeField(auto_now_add=True)),
                ('prof_pic', models.URLField(max_length=300)),
                ('star_user', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'ordering': ['join_date'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('venue_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('venue_name', models.CharField(max_length=100)),
                ('venue_type', models.CharField(choices=[('brewery', 'Brewery'), ('distillery', 'Distillery'), ('winery', 'Winery')], default='brewery', max_length=30)),
                ('is_authenticated', models.BooleanField(default=False)),
                ('hours_of_operation', models.TextField(max_length=300)),
                ('web_url', models.URLField()),
                ('email', models.EmailField(max_length=254)),
                ('twitter_handle', models.CharField(blank=True, max_length=15, null=True)),
                ('insta_handle', models.CharField(blank=True, max_length=30, null=True)),
                ('fb_link', models.URLField(blank=True, max_length=160, null=True)),
                ('phone_num', models.CharField(blank=True, max_length=12, null=True)),
                ('street_address', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=150)),
                ('state', models.CharField(max_length=150)),
                ('zip', models.DecimalField(blank=True, decimal_places=0, max_digits=5, null=True)),
                ('prof_pic', models.URLField(max_length=300)),
                ('tags', models.CharField(blank=True, choices=[('1', 'Outside Seating/Patio'), ('2', 'Pet Friendly'), ('3', 'Great Appetizers'), ('4', 'Large Variety of Draft Beers')], max_length=103, null=True)),
                ('join_date', models.DateTimeField(auto_now_add=True)),
                ('followers_list', models.ManyToManyField(blank=True, related_name='venue_followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['join_date'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('post_img', models.URLField(blank=True, max_length=300, null=True)),
                ('post_text', models.TextField(blank=True, max_length=800, null=True)),
                ('post_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_author', to=settings.AUTH_USER_MODEL)),
                ('post_likers', models.ManyToManyField(blank=True, related_name='post_likers', to=settings.AUTH_USER_MODEL)),
                ('posted_to_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posted_to_user', to=settings.AUTH_USER_MODEL)),
                ('posted_to_venue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posted_to_venue', to='tipsyapp.venue')),
            ],
            options={
                'ordering': ['post_date'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='posts_liked',
            field=models.ManyToManyField(blank=True, related_name='posts_liked', to='tipsyapp.Post'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='user',
            name='users_followed_by_list',
            field=models.ManyToManyField(blank=True, related_name='followed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='users_following_list',
            field=models.ManyToManyField(blank=True, related_name='user_follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='venues_following_list',
            field=models.ManyToManyField(blank=True, related_name='venue_follows', to='tipsyapp.Venue'),
        ),
        migrations.AddConstraint(
            model_name='post',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('posted_to_user__isnull', False), ('posted_to_venue__isnull', True)), models.Q(('posted_to_user__isnull', True), ('posted_to_venue__isnull', False)), _connector='OR'), name='tipsyapp_post_post_on_user_OR_venue'),
        ),
    ]
