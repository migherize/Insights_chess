from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.main, name='main'),
    path('login/', views.signUp, name='login'),
    path('register/', views.register, name='register'),
    path('Home/', views.main, name='Home'),
    path('games/<str:username>/', views.games, name='games'),
    ]