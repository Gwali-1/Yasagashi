# Generated by Django 4.1.3 on 2022-12-13 01:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_listing_available_listing_funished'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='date_listed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
