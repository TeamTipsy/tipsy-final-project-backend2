# Generated by Django 3.2 on 2021-05-04 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipsyapp', '0003_auto_20210502_1543'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='venue',
            constraint=models.UniqueConstraint(fields=('venue_name', 'street_address'), name='unique_venue_location'),
        ),
    ]
