import json
from django.http import JsonResponse
from .models import Listing,Listing_favourites,User
from collections import defaultdict



# def update_profile(Profile_model,bio=None,primary_location=None,profile_image=None):
#     Profile_model.profile_image = profile_image
#     Profile_model.bio = bio
#     Profile_model.primary_location = primary_location
#     try:
#          Profile_model.save()
#          return True
#     except Exception as e:
#         return False





def authenticate_post_form(form):
    exempt = ["csrfmiddlewaretoken","contact"]
    for key,value in form.items():
        if key not in exempt:
            if not value: 
               return False
    return True




def handle_post(request_data):
    try:
        #location
        if request_data["action"] == "location_filter":
            location = request_data.get("location")
            if not location:
                return JsonResponse({
                    "status":"error",
                    "message":"Invalid/no input"
                    })
                                
            listings = Listing.objects.filter(location=location).order_by("date_listed")
            favs = Listing_favourites.objects.filter(user=request_data.get("user"))
        
            return JsonResponse({
                "status":"ok",
                "listings":[listing.serialize() for listing in listings],
                "favs":[fav.listing.id for fav in favs]
                })

                            
        #price
        elif request_data["action"] == "price_filter":
            min_price = request_data.get("min_price")
            max_price = request_data.get("max_price")


            if  min_price is None or max_price is None:
                return JsonResponse({
                    "status":"error",
                    "message":"Invalid/no input"
                    })
            if min_price > max_price:
                return JsonResponse({
                    "status":"error",
                    "message":"Invalid/no input"
                    })

    
            if not isinstance(min_price, (float,int)) or not isinstance(max_price, (float, int)):
                print("not valid input")
                return JsonResponse({
                    "status":"error",
                    "message":"Invalid/no input"
                    })


                                
            listings = Listing.objects.filter(price__range=(min_price,max_price))
            favs = Listing_favourites.objects.filter(user=request_data.get("user"))
            return JsonResponse({
                "status":"ok",
                "listings":[listing.serialize() for listing in listings],
                "favs":[fav.listing.id for fav in favs]

                })

        #sale 
        elif request_data["action"] == "sale_filter":
            listings = Listing.objects.filter(accomodation_type="Sale")
            favs = Listing_favourites.objects.filter(user=request_data.get("user"))

            return JsonResponse({
                "status":"ok",
                "listings":[listing.serialize() for listing in listings],
                "favs":[fav.listing.id for fav in favs]
                })

        #rent
        elif request_data["action"] == "rent_filter":
            listings = Listing.objects.filter(accomodation_type="Rent")
            favs = Listing_favourites.objects.filter(user=request_data.get("user"))
            return JsonResponse({
                "status":"ok",
                "listings":[listing.serialize() for listing in listings],
                "favs":[fav.listing.id for fav in favs]

                }) 

        else:
            return JsonResponse({
                    "status":"error",
                    "message":"Invalid/no input"
                    })


                          

    except Exception as e:
        return JsonResponse({
            "status":"error",
            "message":"could not retrieve error, something happened"
            })





#get number of posts in locations
def get_ad_count(records):
    cities = [x.location for x in records]
    dict_count = defaultdict(int)
    for x in cities:
        dict_count[x] += 1

    return dict_count