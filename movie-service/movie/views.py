# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import generics
from rest_framework.response import Response
from .models import Movie, List, Rating, Tag
from .serializers import MovieSerializer, UserSerializer, ListSerializer, RateSerializer, TagSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from django.contrib.auth import authenticate

logger = logging.getLogger(__name__)

# Create your views here.
    
class MovieViewSet(viewsets.ModelViewSet):
    """
    List all movies or single movie. 
    Create/Update a single movie.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        data = {'name': request.data.get('name'), "user":user.pk}
        serializer = ListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        return List.objects.filter(user=user.pk)

class UserCreateView(generics.CreateAPIView):
    # by-pass python auth
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = ()

    def post(self, request, version):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class SaveMovieView(APIView):

    def post(self, request, *args, **kwargs):
        user = self.request.user
        try:
            movie = Movie.objects.get(pk=kwargs['movie_pk'])
            list = List.objects.get(user=user.pk)
            list.movies.add(movie)
            list.save()
        except Movie.DoesNotExist:
            return Response(data="Movie not found.", status=status.HTTP_400_BAD_REQUEST)
        except List.DoesNotExist:
            return Response(data="List not found.", status=status.HTTP_400_BAD_REQUEST)

        return Response({"status":"success"}, status=status.HTTP_201_CREATED)

class RateMovieView(APIView):

    def post(self, request, *args, **kwargs):
        user = self.request.user
        try:
            rate = kwargs['rate']
            movie = Movie.objects.get(pk=kwargs['movie_pk'])
            rating = Rating.objects.filter(user=user.pk, movie=movie.pk)
            data = {'movie': movie.pk, 'rate': rate, 'user': user.pk}
            serializer = RateSerializer(data=data)

            if len(rating) == 0:
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error":"Not valid"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                r = Rating.objects.get(user=user.pk, movie=movie.pk)
                r.rate = rate
                r.save()

                return Response(RateSerializer(r).data, status=status.HTTP_200_OK)


        except Movie.DoesNotExist:
            return Response({"error":"Movie not found"}, status=status.HTTP_400_BAD_REQUEST)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagMovieView(APIView):

    def post(self, request, *args, **kwargs):
        user = self.request.user
        try:
            tag_id = kwargs['tag_pk']
            movie_id = kwargs['movie_pk']
            tag = Tag.objects.get(pk=tag_id)
            movie = Movie.objects.get(pk=movie_id)
            tag.movie.add(movie)

            return Response({'success':'added tag'}, status=status.HTTP_200_CREATED)
        except Movie.DoesNotExist:
            return Response({'error':'Movie does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        except Tag.DoesNotExist:
            return Response({'error':'Tag does not exist'}, status=status.HTTP_400_BAD_REQUEST)



