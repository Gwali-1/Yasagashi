# Generated by Django 4.1.3 on 2022-12-06 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_profile_sex_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
