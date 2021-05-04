from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic.edit import FormView

from rest_framework import generics, permissions, filters, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ModelViewSet 

from .permissions import IsPostAuthorOrReadOnly, IsVenueOwnerOrReadOnly
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
    parser_classes = [MultiPartParser, JSONParser]
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
    # parser_classes = [MultiPartParser, JSONParser]
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
    
    def perform_create(self, serializer):
        serializer.save(post_author = self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, JSONParser]
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


'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
new image upload classes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
''' 


class ImageVenueSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Venue.objects.all()
    serializer_class=VenueSerializer
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        return self.list(request)


    def post(self, request, format=None):
        print("**********  This is what our request data looks like:", request.data)
        temp_serializer = self.get_serializer(data = json.loads(request.data.__getitem__('jsondata')))
        print("********** and our initial serializer, pre additions:", temp_serializer)
        print("~~~pre", temp_serializer.initial_data)
        temp_serializer.initial_data['v_prof_pic']=request.data.__getitem__('v_prof_pic')
        print("~~~post", temp_serializer.initial_data)


        debug4amy = request.data.__getitem__('v_prof_pic')
        debug4amy.save()
        # if request.data.__contains__('v_prof_pic'):
        #     v_prof_pic_file = request.data.__getitem__('v_prof_pic')
        #     temp_serializer.initial_data['v_prof_pic'].save(v_prof_pic_file.name, v_prof_pic_file, save=True)
        #     # request.data.v_prof_pic.save(v_prof_pic_file.name, v_prof_pic_file, save=True)
        #     print("Lemme ALSO see somethin real quick", v_prof_pic_file.url)
        #     vpp_url = v_prof_pic_file.url
            # TKTKTK.v_prof_pic.save(v_prof_pic_file.name, v_prof_pic_file, save=True)
            # print("did the profile pic save?", TKTKTK.v_prof_pic)
        temp_serializer.is_valid(raise_exception=True)
        self.perform_create(temp_serializer)
        print("checking what temp serializer looks like now:", temp_serializer)
        # return Response({'received data': request.data})        
        return Response(
            temp_serializer.data
        )
    def perform_create(self, serializer):
        serializer.save(venue_added_by = self.request.user)



'''
        if request.data.__contains__('v_prof_pic') and request.data.__contains__('v_banner_img'):
            v_prof_pic_file = request.data.__getitem__('v_prof_pic')
            v_banner_img_file = request.data.__getitem__('v_banner_img')
            print("!!!!!!!!!!!!", v_prof_pic_file)
            # TKTKTK.v_prof_pic.save(v_prof_pic_file.name, v_prof_pic_file, save=True)
            # print("did the profile pic save?", TKTKTK.v_prof_pic)
            vpp_url = temp_serializer.v_prof_pic.url



        if request.data.__contains__('v_prof_pic'):
            v_prof_pic_file = request.data.__getitem__('v_prof_pic')
            thisvenue.v_prof_pic.save(v_prof_pic_file.name, v_prof_pic_file, save=True)
            print("did the profile pic save?", thisvenue.v_prof_pic)
            pp_url = thisvenue.v_prof_pic.url
            kwarglist.append(pp_url)
        if request.data.__contains__('v_banner_img'):
            v_banner_img_file = request.data.__getitem__('v_banner_img')
            thisvenue.v_banner_img.save(v_banner_img_file.name, v_banner_img_file, save=True)
            print("did the banner image save?", thisvenue.v_banner_img)
            bi_url = thisvenue.v_banner_img.url
            kwarglist.append(pp_url)

'''