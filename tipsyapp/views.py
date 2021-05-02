from django.shortcuts import render, get_object_or_404
from .forms import MyUserCreationForm, MyUserChangeForm #, Upload, VenueUpload, PostUpload
from django.views.generic.edit import FormView
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPostAuthorOrReadOnly, IsVenueOwnerOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser
from rest_framework.decorators import action
from .models import User, Venue, Post, CheckIn
from .serializers import UserSerializer, VenueSerializer, PostSerializer, CheckInSerializer
from .decorators import unauthenticated_user, allowed_users
import json
import uuid


class UserList(generics.ListCreateAPIView):
    queryset= User.objects.all()
    serializer_class = UserSerializer    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['username', 'first_name', 'last_name',]
    filter_backends = (filters.SearchFilter,)


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
    search_fields = ['venue_name', 'city', 'state', 'zip', 'twitter_handle', 'insta_handle']
    filter_backends = (filters.SearchFilter,)

    def perform_create(self, serializer):
        serializer.save(venue_added_by = self.request.user)


class VenueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsVenueOwnerOrReadOnly
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
    search_fields = ['post_text',]
    filter_backends = (filters.SearchFilter,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser]

    @action(detail=False, methods=['post'])
    def image(self, request, id=None):
        imagefile = request.data.__getitem__('img')
        # json_input = json.load(request.data.__getitem__('jsondata'))
        # print("json input:", json_input)
        user = self.get_object()
        user.imagefile.save(imagefile.name, imagefile, save=True)
        print("image saved- in theory")
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=201)
    def get_parser_classes(self):
        if type(self.request.data)==dict:
            return [JSONParser]
        return [MultiPartParser]
    def perform_create(self, serializer):
        print("ZZZZ", type(self.request.data))
        print(self.request.data)
        json_input = self.request.data.__getitem__('jsondata')
        print("json_input:", json_input)
        willitload = json.loads(json_input)
        print("will it load?", willitload)
        p2v = uuid.UUID(willitload['posted_to_venue'])
        print("willitload[posted_to_venue]:", p2v)
        print("willitload[posted_to_venue] TYPE:", type(p2v))
        # print("json_input[0]:", json_input[0])
        print("and here is how we get the image object", self.request.data.__getitem__('img'))
        # img = self.request.data.__getitem__('img')
        # img.save()
        # print("img saved hopefully:", img)
        serializer.save(post_author = self.request.user, posted_to_venue = p2v)
        # serializer.save(post_author = self.request.user, posted_to_venue = json_input['posted_to_venue'] )



class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FileUploadParser, JSONParser]
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsPostAuthorOrReadOnly,
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



class CheckInList(generics.ListCreateAPIView):
    # pagination_class = CheckInPagination
    queryset= CheckIn.objects.all()
    serializer_class = CheckInSerializer    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(checkin_user = self.request.user)


class CheckInDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        ]


# class UploadPost(generics.ListCreateAPIView):
#     queryset= Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]


    # template_name = 'index.html'
    # form_class = Upload
    # success_url = '/'

    # def form_valid(self, form):
    #     form.save()
    #     print(form.cleaned_data)
    #     return super().form_valid(form)

