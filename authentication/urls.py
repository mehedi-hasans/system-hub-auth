from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='loginPage'),
    path('signup', views.signupPage, name='signupPage'),
    path('index', views.index, name='index'),
    path('logOut', views.logOut, name='logOut'),
    #Profile Update
    path('profile', views.profile, name='profile'),
    path('profile/update', views.profileUpdate, name='profileUpdate'),
]
