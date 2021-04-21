# Generated by Django 3.2 on 2021-04-21 15:04

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('city', models.CharField(max_length=150)),
                ('state', models.CharField(max_length=150)),
                ('bio_text', models.TextField(blank=True, max_length=500, null=True)),
                ('join_date', models.DateTimeField(auto_now_add=True)),
                ('prof_pic', models.URLField(max_length=300)),
                ('star_user', models.BooleanField(default=False)),
                ('users_following_num', models.IntegerField(default=0)),
                ('venues_following_num', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('users_followed_by_list', models.ManyToManyField(blank=True, related_name='followed_by', to=settings.AUTH_USER_MODEL)),
                ('users_following_list', models.ManyToManyField(blank=True, related_name='user_follows', to=settings.AUTH_USER_MODEL)),
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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue_name', models.CharField(max_length=100)),
                ('venue_type', models.CharField(choices=[('br', 'Brewery'), ('ds', 'Distillery'), ('wn', 'Winery')], default='br', max_length=30)),
                ('is_authenticated', models.BooleanField(default=False)),
                ('hours_of_operation', models.TextField(max_length=300)),
                ('web_url', models.URLField()),
                ('email', models.EmailField(max_length=254)),
                ('street_address', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=150)),
                ('state', models.CharField(max_length=150)),
                ('prof_pic', models.URLField(max_length=300)),
                ('followers_num', models.IntegerField(default=0)),
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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_img', models.URLField(blank=True, max_length=300)),
                ('post_text', models.TextField(blank=True, max_length=800, null=True)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('post_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('posted_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tipsyapp.venue')),
            ],
            options={
                'ordering': ['post_date'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='venues_following_list',
            field=models.ManyToManyField(blank=True, related_name='venue_follows', to='tipsyapp.Venue'),
        ),
    ]
