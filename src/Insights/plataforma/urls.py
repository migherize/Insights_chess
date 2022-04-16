from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.signUp, name='login'),
    path('Home/', views.Home, name='Home'),
    ]