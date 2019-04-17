# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from rest_framework import generics
from rest_framework.response import Response
from .models import Movie, List
from .serializers import MovieSerializer, UserSerializer, ListSerializer
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
        movie = Movie.objects.get(pk=kwargs['movie_pk'])
        list = List.objects.get(user=user.pk)
        list.movies.add(movie)
        if list.save():
            return Response({"status":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
