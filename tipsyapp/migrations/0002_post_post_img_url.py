# Generated by Django 3.2 on 2021-05-02 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipsyapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_img_url',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
    ]
