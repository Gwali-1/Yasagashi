from django.shortcuts import render,redirect
from  django.http import HttpResponse, HttpResponseRedirect
import json


## pyrebase initalization

# with open("config.json","r") as f:
#     firebaseConfig = json.load(f)




## Create your views here.

def index(request):
    return HttpResponse("index view")


def signup(request):
    return render(request,"main/register.html")

def login(request):
    return render(request,"main/login.html")

def logout(request):
    return HttpResponse("logged out")