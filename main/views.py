from django.shortcuts import render,redirect
from  django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User,Listing,Profile
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from . import  firebase_auth, firebase_storage
import uuid
import datetime
from .helpers import authenticate_post_form
from django.db import transaction,IntegrityError





USER_OBJ={}


## Create your views here.

def index(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request,"main/index.html",{"profile":profile})


    return render(request,"main/index.html")



    

#register create user account on firrbase  -> store in database -> profile settings-> login
def signup(request):

    if request.method == "POST":
        print("ok")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmation")

        print("====>",username,email,password,confirm_password)
        
       
        #authenticate user input
        if not username or not email or not password or not confirm_password:
            print("not hit")
            messages.error(request,"provide valid details")
            return render(request,"main/register.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request,"Account with this email already exist")
            return render(request,"main/register.html")
        
        if password != confirm_password:
            print("confirm hit")
            messages.error(request,"passwords do not match")
            return render(request,"main/register.html")
        

        #firebase 
        try:
            user = firebase_auth.create_user_with_email_and_password(email,password)
            USER_OBJ["firebase_user"]=user
        except Exception as e:
            messages.error(request,"something happened , try again later")
            return HttpResponseRedirect(reverse("signin"))
   

        #database
        try:
            new_user = User.objects.create_user(username,email,password)
            new_user.save()
            valid_user = authenticate(request,username=username,password=password)
            new_profile = Profile.objects.create(user=valid_user)
            new_profile.save()
            login(request,valid_user)
            messages.success(request,"account created")
            password,confirm_password = ""
            return HttpResponseRedirect(reverse("profile"))

        except Exception as e:
            print(e)
            messages.error(request,"could not add user")
            return HttpResponseRedirect(reverse("signup"))
    
        
    return render(request,"main/register.html")











def signin(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        print(email,password)
        if not email or not password:
            messages.error(request,"provide valid input")
            return HttpResponseRedirect(reverse("signin"))

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request,"invalid email or password")
            return HttpResponseRedirect(reverse("signin"))

        ##chek password

        check_user = authenticate(request,username=user.username,password=password)
        if check_user is None:
            messages.error(request,"invalid email or password")
            return HttpResponseRedirect(reverse("signin"))


        #firebase
        try:
            user_firebase = firebase_auth.sign_in_with_email_and_password(email,password)
            USER_OBJ["firebase_user"] = user_firebase
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        except Exception as e:
            return render(request,"main/login_error.html",{"error":e})

        
       
    return render(request,"main/login.html")











@login_required
def profile_settings(request):
    profile = Profile.objects.get(user=request.user)


    #authenticate user input

    if request.method == "POST":
        if not USER_OBJ:
            logout(request)
            messages.info(request,"Log in to edit profile")
            return HttpResponseRedirect(reverse("signin"))

       

        if not request.FILES.get("image"):
            print("no image")
            image = profile.profile_image
            location = request.POST.get("location")
            bio = request.POST.get("bio")
            profile.profile_image = image
            profile.bio = bio
            profile.primary_location = location
            profile.save()

            return HttpResponseRedirect(reverse("profile"))



        image = request.FILES.get("image")
        try:
            ##firebase storage
            user = firebase_auth.refresh(USER_OBJ["firebase_user"]["refreshToken"])
            image_name = f"{request.user.username}-profile-{datetime.datetime.now()}-{uuid.uuid1()}"
            firebase_storage.child(f"profile/{image_name}").put(image)
            image_url = firebase_storage.child(f"profile/{image_name}").get_url(user['idToken'])
                
            #database
            with transaction.atomic():
                location = request.POST.get("location")
                bio = request.POST.get("bio")
                profile.profile_image = image_url
                profile.bio = bio
                profile.primary_location = location
                profile.save()
            return HttpResponseRedirect(reverse("profile"))

        except Exception as e:
            messages.info(request,"Something happened , try again later")
            return HttpResponseRedirect(reverse("profile"))
        
    
    return render(request,"main/profile_settings.html",{"profile":profile})





def post(request):

    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        if not USER_OBJ:
            logout(request)
            messages.info(request,"Log in to make a post")
            return HttpResponseRedirect(reverse("signin"))

        print(request.FILES)
        print(request.FILES.getlist("image"))


        accomodation_type = request.POST.get("type")
        price = request.POST.get("price")
        location = request.POST.get("location")
        description = request.POST.get("description")
        contact = request.POST.get("type")
        image = request.FILES.get("image")

        if not authenticate_post_form(request.POST):
            messages.error(request,"Fill in  all required fields")
            return HttpResponseRedirect(reverse("post"))

        # if len(request.FILES.getlist < 2):
        #     pass

        #firebase
        urls = []
        user = firebase_auth.refresh(USER_OBJ["firebase_user"]["refreshToken"])
        for image in request.FILES.getlist("image"):
            try:
                image_name = f"{request.user.username}-profile-{datetime.datetime.now()}-{uuid.uuid1()}"
                firebase_storage.child(f"accomodation_post/{image_name}").put(image)
                urls.append(firebase_storage.child(f"profile/{image_name}").get_url(user['idToken']))

            except Exception as e:
                messages.info(request, "could not add Listing , try again later")
                return HttpResponseRedirect(reverse("post"))

        #database
        try:
            with transaction.atomic():
                image_url = "|".join(x for x in urls)
                print(image_url)
                new_Listing = Listing.objects.create(user=request.user, accomodation_type=accomodation_type,price=price,
                location=location,description=description.strip(),contact=contact,image=image_url)
                new_Listing.save()
                urls.clear()
        except IntegrityError:
            messages.info(request, "could not add Listing , try again later")
            return HttpResponseRedirect(reverse("post"))



        messages.success(request,"Listing added")
        return HttpResponseRedirect(reverse("index"))


        
    return render(request,"main/post.html",{"profile":profile})





@login_required
def listing(request):
    profile = Profile.objects.get(user=request.user)
    return render(request,"main/listing.html",{"profile":profile})




@login_required
def signout(request):

    logout(request)
    USER_OBJ.clear()
    return redirect("signin")
