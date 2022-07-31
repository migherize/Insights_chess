from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)