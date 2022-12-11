



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