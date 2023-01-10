from django.contrib import admin
from .models import User,Listing_favourites,Listing,Profile

# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Listing)
admin.site.register(Listing_favourites)

