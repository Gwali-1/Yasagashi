import json
from django.http import JsonResponse
from .models import Listing



def update_profile(Profile_model,bio=None,primary_location=None,profile_image=None):
    Profile_model.profile_image = profile_image
    Profile_model.bio = bio
    Profile_model.primary_location = primary_location
    try:
         Profile_model.save()
         return True
    except Exception as e:
        return False





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
        if request_data["action"] == "loaction_filter":
            location = request_data.get("location")
            if not location:
                return JsonResponse({
                    "status":"error",
                    "message":"Invalid/no input"
                })
                    
            listings = Listing.objects.filter(location=location).order_by("date_listed")
            return JsonResponse({
                "status":"ok",
                "listings":[listing.serialize for listing in listings]
                })
                
        #price
        elif request_data["action"] == "price_filter":
            min_price = request_data.get("min_price")
            max_price = request_data.get("max_price")

            print(min_price,max_price)

            if not min_price or not max_price:
                return JsonResponse({
                    "status":"error",
                    "message":"Invalid/no input"
                    })
                        
            listings = Listing.objects.filter(price__range=(min_price,max_price))

            return JsonResponse({
                "status":"ok",
                "listings":[listing.serialize for listing in listings]
                })

        #sale 
        elif request_data["action"] == "sale_filter":
            listings = Listing.objects.filter(accomodation_type="sale")

            return JsonResponse({
                "status":"ok",
                "listings":[listing.serialize for listing in listings]
                })

        #rent
        elif request_data["action"] == "rent_filter":
            listings = Listing.objects.filter(accomodation_type="rent")
            return JsonResponse({
                "status":"ok",
                "listings":[listing.serialize for listing in listings]
                })
                        

    except Exception as e:
        print(e)
        return JsonResponse({
            "status":"error",
            "message":"could not retrieve error, something happened"
        })
