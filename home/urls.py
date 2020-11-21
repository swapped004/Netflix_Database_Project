"""NETFLIX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home_notLoggedIn),
    path('home/', views.home_notLoggedIn, name="homepage"),
    path('home/logout/', views.log_out, name="logout"),
    path('genre/<str:genre_name>/', views.genre, name="genre_view"),
    path('shows/<str:show_type>/', views.shows, name="shows_view"),
    path('movies/', views.movies, name="movies_view"),
    path('movies/<str:show_id>/', views.single_show, name="single_show"),
    path('series/<str:series_identifier>/', views.single_series, name="single_series"),


]
