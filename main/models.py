from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


# Create your models here.

class User(AbstractUser):
    pass


class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="profile")
    bio=models.TextField(blank=True)
    primary_location=models.CharField(max_length=200,blank=True)
    profile_image=models.TextField(default="")
    Agent=models.BooleanField(default=False)
    email_verified=models.BooleanField(default=False)
    credibilty=models.IntegerField(default=0)



class Listings(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="listings")
    image=models.TextField(default="")
    date_listed=models.DateTimeField(default=datetime.datetime.now.strftime("%m/%d/%Y, %H:%M:%S"))
    available=models.BooleanField(default=False)
    description=models.TextField()
    location=models.CharField(max_length=100)
    accomodation_type=models.CharField(max_length=100)


class Listing_favourites(models.Model):
    listing=models.ForeignKey(Listings,on_delete=models.CASCADE,related_name=("favourited_by"))
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name=("favourites"))



#when you give cred
class Agents_favourite(models.Model):
    agent=models.ForeignKey(User,on_delete=models.CASCADE,related_name="faved_agents")
    user=models.ForeignKey(User,on_delete=models.CASCADE)






