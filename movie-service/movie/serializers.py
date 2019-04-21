from rest_framework import serializers
from .models import Movie, List, Tag, Rating
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', "title", "director")
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

class ListSerializer(serializers.ModelSerializer):
    movies = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)

    class Meta:
        model = List
        fields = ('id','name', 'user', 'movies')

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rate', 'movie', 'user')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'movie')
