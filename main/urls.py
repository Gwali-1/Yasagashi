from django.urls import path
from . import views


urlpatterns = [
    path("",views.index,name="index"),
    path("home/page_num/<int:id>",views.home,name="home"),
    path("signup",views.signup,name="signup"),
    path("signin",views.signin,name="signin"),
    path("signout",views.signout,name="signout"),
    path("profile",views.profile_settings,name="profile"),
    path("add_listing",views.post,name="post"),
    path("listing/<str:id>",views.listing,name="listing")
    
]
