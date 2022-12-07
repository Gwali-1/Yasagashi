from django.shortcuts import render,redirect
from  django.http import HttpResponse, HttpResponseRedirect
import json
from .models import User,Listings,Profile
from django.contrib import messages
import os
from . import  firebase_auth, firebase_storage







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
        
        if password != confirm_password:
            print("confirm hit")
            messages.error(request,"passwords do not match")
            return render(request,"main/register.html")
        

        #firebase 
        try:
            user = firebase_auth.create_user_with_email_and_password(email,password)
            user_info = firebase_auth.get_account_info()
            print(user_info)
        except Exception as e:
            print(type(e))
            # print(e)

         #database


    return render(request,"main/register.html")

def login(request):
    return render(request,"main/login.html")

def logout(request):
    return HttpResponse("logged out")