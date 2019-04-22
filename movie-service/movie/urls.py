"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
# from .views import ListMoviesView, RetrieveMovieView
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, UserCreateView, LoginView, ListViewSet, SaveMovieView, RateMovieView, TagViewSet, TagMovieView



router = DefaultRouter()
router.register('movie', MovieViewSet, base_name='movie')
router.register('list', ListViewSet, base_name='list')
router.register('tag', TagViewSet, base_name='tag')

urlpatterns = [
    # path('movies/', ListMoviesView.as_view(), name="movies-all"),
    # path('movies/<int:pk>/', RetrieveMovieView.as_view(), name="movies-detail")
    path("user/", UserCreateView.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    path("movie/<int:movie_pk>/save/", SaveMovieView.as_view(), name="save_movie"),
    path("movie/<int:movie_pk>/rate/<int:rate>", RateMovieView.as_view(), name="rate_movie"),
    path('movie/<int:movie_pk>/tag/<int:tag_pk>', TagMovieView.as_view(), name="tag_movie")
]

urlpatterns += router.urls