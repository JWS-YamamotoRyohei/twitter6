"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'twitter'

urlpatterns = [
    path('', views.index, name='index'),
    path('tweetlist/', views.tweetlist, name='tweetlist'),
    path('favoritelist/', views.favoritelist, name='favoritelist'),
    path('tweet_new/', views.tweet_new, name='tweet_new'),
    path('del_tweet/<int:tweet_id>/', views.del_tweet, name='del_tweet'),
    path('<int:tweet_id>/', views.detail, name='detail'),
    # path('<int:tweet_id>/results/', views.results, name='results'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="twitter/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="twitter:index"), name='logout'),
    path('<slug:username>', views.ProfileDetailView.as_view(), name='profile'),
    path('<slug:username>/follow', views.follow_view, name='follow'),
    path('<slug:username>/unfollow', views.unfollow_view, name='unfollow'),
    path('add-favorite/<int:favorite_tweet_id>/', views.add_favorite, name='add_favorite'),
    path('del-favorite/<int:favorite_tweet_id>/', views.del_favorite, name='del_favorite'),
]


