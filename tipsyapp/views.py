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
    # parser_classes = [MultiPartParser, FileUploadParser, JSONParser]
    parser_classes = [JSONParser]

    @action(detail=False, methods=['post'])
    def get_parser_classes(self):
        print("ZZZZ", type(self.request.data))
        if type(self.request.data)==dict:
            return [JSONParser]
        return [MultiPartParser]
    def perform_create(self, serializer):
        print("ZZZZ", type(self.request.data))
        # print(type(self.request.data)==QueryDict)
        print(self.request.data)
        serializer.save(post_author = self.request.user)


    # def post_image(self, request, id=None):
    #     print("ZZZZZZZZZZZZZZZZZ")
    #     print("ZZZZZZZZZZZZZZZZZ")
    #     print("ZZZZZZZZZZZZZZZZZ")
    #     print("ZZZZZZZZZZZZZZZZZ")
    #     print(request.data)
    #     if 'image1' not in request.data:
    #         raise ParseError("You didn't add an image- I should fix this")
    #     file = request.data['image1']
    #     user = self.get_object()
    #     user.post_image.save(file.name, file, save=True)
    #     serializer = self.get_serializer(user)
    #     return Response(serializer.data, status=201)       

    
    
    # def perform_create(self, serializer):
    #     serializer.save(post_author = self.request.user)
    # def post_image(self, request, id=None):
    #     if 'file' not in request.data:
    #         raise ParseError("You didn't add an image- I should fix this")
    #     file = request.data['file']
    #     user = self.get_object()
    #     user.post_image.save(file.name, file, save=True)
    #     serializer = self.get_serializer(user)
    #     return Response(serializer.data, status=201)       


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

