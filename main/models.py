from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone


# Create your models here.

class User(AbstractUser):
    pass


class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="profile_info")
    bio=models.TextField(blank=True)
    primary_location=models.CharField(max_length=200,blank=True, null=True)
    profile_image=models.TextField(default="https://firebasestorage.googleapis.com/v0/b/web-projs-122ec.appspot.com/o/profile%2Fundraw_Male_avatar_re_y880.png?alt=media&token=ad0ac38c-5b35-4bb4-92bc-1b3a377f66e0")
    Agent=models.BooleanField(default=False)
    email_verified=models.BooleanField(default=False)
    credibilty=models.IntegerField(default=0)
    

    def __str__(self):
        return f"{self.user.username} Profile"



class Listing(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="listings")
    image=models.TextField(default="")
    date_listed=models.DateTimeField(default=timezone.now)
    description=models.TextField()
    location=models.CharField(max_length=100)
    price=models.FloatField(default=0.00)
    accomodation_type=models.CharField(max_length=100)
    contact=models.CharField(max_length=15,blank=True,null=True)
    furnished=models.BooleanField(default=True)

    def __str__(self):
        return f"Listing by {self.user.username}"


class Listing_favourites(models.Model):
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name=("favourited_by"))
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name=("favourites"))

    def __str__(self):
        return f"Listing favourited by {self.user.username}"


#when you give cred
class Agents_favourite(models.Model):
    agent=models.ForeignKey(User,on_delete=models.CASCADE,related_name="faved_agents")
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f" Agent {self.user.username} cred  by {self.user.username}"






