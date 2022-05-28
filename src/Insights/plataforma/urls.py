from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.main, name='main'),
    path('login/', views.signUp, name='login'),
    path('register/', views.register, name='register'),
    path('register_lichess/', views.register_lichess, name='register_lichess'),
    path('Home/', views.main, name='Home'),
    path('logout/', views.signOut, name='logout'),
    path('view_games/<str:username>/', views.view_games, name='view_games'),
    path('games/<str:username>/', views.games, name='games'),
    path('estadisticas/<str:username>/', views.estadisticas, name='estadisticas'),
    path('insight/<str:username>/', views.insight, name='insight'),
    ]