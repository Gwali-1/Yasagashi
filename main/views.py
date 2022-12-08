from django.shortcuts import render,redirect
from  django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User,Listings,Profile
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from . import  firebase_auth, firebase_storage
import uuid
import datetime




USER_OBJ={}


## Create your views here.

def index(request):
    return HttpResponse("index view")



    

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
            print(e)
   

        #database
        try:
            new_user = User.objects.create_user(username,email,password)
            new_user.save()
            valid_user = authenticate(request,username=username,password=password)
            new_profile = Profile.objects.create(user=valid_user)
            new_profile.save()
            
            login(request,valid_user)
            messages.success(request,"account created")
            return HttpResponseRedirect(reverse("profile"))
        except Exception as e:
            print(e)
            messages.error(request,"could not add user")
            return HttpResponseRedirect(reverse("signup"))
    
        


    return render(request,"main/register.html")











def signin(request):
    print(USER_OBJ)
    return render(request,"main/login.html")

def logout(request):
    return HttpResponse("logged out")



def profile_settings(request):
    profile = Profile.objects.get(user=request.user)


    #authenticate user input

    if request.method == "POST":
        print(USER_OBJ)
        print( request.POST)
        user = firebase_auth.refresh(USER_OBJ["firebase_user"]["refreshToken"])

        if not request.FILES.get("image"):
            image = profile.profile_image
            location = request.POST.get("location")
            bio = request.POST.get("bio")
            profile.profile_image = image
            profile.bio = bio
            profile.primary_location = location
            profile.save()

            return HttpResponseRedirect(reverse("profile"))



        image = request.FILES.get("image")
        ##firebase storage
        image_name = f"{request.user.username}-profile-{datetime.datetime.now()}-{uuid.uuid1()}"
        firebase_storage.child(f"profile/{image_name}").put(image)
        image_url = firebase_storage.child(f"profile/{image_name}").get_url(user['idToken'])
        
        #database
        location = request.POST.get("location")
        bio = request.POST.get("bio")
        profile.profile_image = image_url
        profile.bio = bio
        profile.primary_location = location
        profile.save()

        return HttpResponseRedirect(reverse("profile"))

    
    return render(request,"main/profile_settings.html",{"profile":profile})