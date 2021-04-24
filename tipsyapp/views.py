from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from .permissions import IsPostAuthorOrReadOnly
from rest_framework.exceptions import ValidationError
from .models import User, Venue, Post
from .serializers import UserSerializer, VenueSerializer, PostSerializer


class UserList(generics.ListCreateAPIView):
    queryset= User.objects.all()
    serializer_class = UserSerializer    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        ]
        
    def put(self, request, pk):
        obj = User.objects.get(user_id=pk)
        if request.user not in obj.users_followed_by_list.all():
            obj.users_followed_by_list.add(request.user)
            request.user.users_following_list.add(obj.user_id)
            return Response({'detail': 'User Followed'})
        elif request.user in obj.users_followed_by_list.all():
            obj.users_followed_by_list.remove(request.user)
            request.user.users_following_list.remove(obj.user_id)
            return Response({'detail': 'User Unfollowed'})    



class VenueList(generics.ListCreateAPIView):
    queryset= Venue.objects.all()
    serializer_class = VenueSerializer    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def perform_create(self, serializer):
    #     serializer.save(venue_added_by = self.request.user)

class VenueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        ]

    def put(self, request, pk):
        obj = Venue.objects.get(venue_id=pk)
        if request.user not in obj.followers_list.all():
            obj.followers_list.add(request.user)
            request.user.venues_following_list.add(obj.venue_id)
            return Response({'detail': 'Venue Followed'})
        elif request.user in obj.followers_list.all():
            obj.followers_list.remove(request.user)
            request.user.venues_following_list.remove(obj.venue_id)
            return Response({'detail': 'Venue Unfollowed'})
            

        return Response({'detail': 'something went wrong with your follow request. are you passing a token?'})


class PostList(generics.ListCreateAPIView):
    queryset= Post.objects.all()
    serializer_class = PostSerializer    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(post_author = self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        # IsPostAuthorOrReadOnly,
        ]

    def put(self, request, pk):
        obj = Post.objects.get(post_id=pk)
        if request.user not in obj.post_likers.all():
            obj.post_likers.add(request.user)
            request.user.posts_liked.add(obj.post_id)
            return Response({'detail': 'Post Liked'})
        elif request.user in obj.post_likers.all():
            obj.post_likers.remove(request.user)
            request.user.posts_liked.remove(obj.post_id)
            return Response({'detail': 'Post Unliked'})
            

        return Response({'detail': 'something went wrong with your follow request. are you passing a token?'})


