from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='loginPage'),
    path('signup', views.signupPage, name='signupPage'),
    path('index', views.index, name='index'),
]
