from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from songs.models import *

from .permissions import *
from .serializers import *


class SongsApiList(generics.ListCreateAPIView):
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class SongsApiUpdate(generics.RetrieveUpdateAPIView):
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly, )


class SongsApiDestroy(generics.RetrieveDestroyAPIView):
    queryset = Songs.objects.all()
    serializer_class = SongsSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly, )



class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
