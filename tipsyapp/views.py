from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import User, Venue, Post
from .serializers import UserSerializer, VenueSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    
class VenueList(generics.ListCreateAPIView):
    queryset= Venue.objects.all()
    serializer_class = VenueSerializer    
    permission_classes = [IsAuthenticatedOrReadOnly]


class VenueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

