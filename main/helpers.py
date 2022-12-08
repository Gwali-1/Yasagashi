



def update_profile(Profile_model,bio=None,primary_location=None,profile_image=None):
    Profile_model.profile_image = profile_image
    Profile_model.bio = bio
    Profile_model.primary_location = primary_location
    try:
         Profile_model.save()
         return True
    except Exception as e:
        return False