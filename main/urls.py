from django.urls import path
from . import views


urlpatterns = [
    path("",views.index,name="index"),
    path("signup",views.signup,name="signup"),
    path("login",views.signin,name="signin"),
    path("logout",views.logout,name="logout"),
    path("profile",views.profile_settings,name="profile")
    
]
