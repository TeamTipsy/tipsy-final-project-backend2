# Generated by Django 3.2 on 2021-04-24 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipsyapp', '0004_venue_venue_added_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='prof_pic',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
    ]
