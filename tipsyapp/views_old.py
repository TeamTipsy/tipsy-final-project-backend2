from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic.edit import FormView
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPostAuthorOrReadOnly, IsVenueOwnerOrReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser, FileUploadParser
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin
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
    
    # @action(detail=True, methods=['patch'])
    # def patch(self, request, pk):
    #     user = self.request.user
    #     serializer = UserSerializer(data = json.loads(request.data.__getitem__('jsondata')), partial=True)
    #     if request.data.__contains__('prof_pic'):
    #         prof_pic_file = request.data.__getitem__('prof_pic')
    #         user.prof_pic.save(prof_pic_file.name, prof_pic_file, save=True)
    #         print("did the profile pic save?", user.prof_pic)
    #         pp_url = user.prof_pic.url
    #     if request.data.__contains__('banner_img'):
    #         banner_img_file = request.data.__getitem__('banner_img')
    #         user.banner_img.save(banner_img_file.name, banner_img_file, save=True)
    #         print("did the banner image save?", user.banner_img)
    #         bi_url = user.banner_img.url
    #     if serializer.is_valid():
    #         serializer.save(prof_pic_url = pp_url, banner_img_url= bi_url )
    #         return JsonResponse(serializer.data)
    #     print('serializer wasnt valid dude')
    #     return JsonResponse(serializer.errors, status=400)    
    # def get_parser_classes(self):
    #     if type(self.request.data)==dict:
    #         return [JSONParser]
    #     return [MultiPartParser]



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

    # @action(detail=True, methods=['patch'])
    # def patch(self, request, pk):
    #     thisvenue = Venue.objects.get(venue_id=pk)
    #     serializer = VenueSerializer(data = json.loads(request.data.__getitem__('jsondata')))
    #     kwarglist = []
    #     if request.data.__contains__('v_prof_pic'):
    #         v_prof_pic_file = request.data.__getitem__('v_prof_pic')
    #         thisvenue.v_prof_pic.save(v_prof_pic_file.name, v_prof_pic_file, save=True)
    #         print("did the profile pic save?", thisvenue.v_prof_pic)
    #         pp_url = thisvenue.v_prof_pic.url
    #         kwarglist.append(pp_url)
    #     if request.data.__contains__('v_banner_img'):
    #         v_banner_img_file = request.data.__getitem__('v_banner_img')
    #         thisvenue.v_banner_img.save(v_banner_img_file.name, v_banner_img_file, save=True)
    #         print("did the banner image save?", thisvenue.v_banner_img)
    #         bi_url = thisvenue.v_banner_img.url
    #         kwarglist.append(pp_url)
    #     if serializer.is_valid():
    #         serializer.save(v_prof_pic_url = pp_url, v_banner_img_url= bi_url)
    #         return self.partial_update(request, serializer.data)
    #     print('serializer wasnt valid dude')
    #     return JsonResponse(serializer.errors, status=400)    
    # def get_parser_classes(self):
    #     if type(self.request.data)==dict:
    #         return [JSONParser]
    #     return [MultiPartParser]


class PostList(generics.ListCreateAPIView):
    queryset= Post.objects.all()
    serializer_class = PostSerializer    
    search_fields = ['post_text',]
    filter_backends = (filters.SearchFilter,)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, MultiPartParser]


    # def post(self, request, format=None):
    #     print("zzzzzz", request.data)
    #     serializer = PostSerializer(data = json.loads(request.data.__getitem__('jsondata')))
    #     imagefile = request.data.__getitem__('img')
    #     thispost = self.get_this_post()
    #     thispost.post_img_1.save(imagefile.name, imagefile, save=True)

    #     if serializer.is_valid():
    #         serializer.save(post_author=self.request.user)
    #         return JsonResponse(serializer.data)
    #     print('serializer wasnt valid dude')
    #     return JsonResponse(serializer.errors, status=400)    
    # def get_this_post(self):
    #     print("I hate coding", self.get_queryset())
    #     post_instance = get_object_or_404(
    #         self.get_queryset(), pk=self.kwargs["post_id"])
    #     print(post_instance)
    #     return post_instance

    

'''
    def post(self, request, format=None):
        print("zzzzzz", request.data)
        serializer = PostSerializer(data = json.loads(request.data.__getitem__('jsondata')))
        imagefile = request.data.__getitem__('img')
        user = self.request.user
        print("USER:", user)

        if serializer.is_valid():
            user.prof_pic.save(imagefile.name, imagefile, save=True)
            serializer.save(post_author=self.request.user)
            return JsonResponse(serializer.data)
        print('serializer wasnt valid dude')
        return JsonResponse(serializer.errors, status=400)    
'''

#why is my computer reading this

'''    
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
'''


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

    # @action(detail=True, methods=['patch'])
    # def patch(self, request, pk):
    #     thispost = Post.objects.get(post_id=pk)
    #     print("zzzzzz", request.data)
    #     serializer = PostSerializer(data = json.loads(request.data.__getitem__('jsondata')))
    #     imagefile = request.data.__getitem__('img')
    #     print('thispost:', thispost)
    #     thispost.post_img_1.save(imagefile.name, imagefile, save=True)
    #     print("did the image save?", thispost.post_img_1)
    #     image_url = thispost.post_img_1.url
    #     if serializer.is_valid():
    #         serializer.save(post_author=self.request.user, post_img_url = image_url )
    #         return JsonResponse(serializer.data)
    #     print('serializer wasnt valid dude')
    #     return JsonResponse(serializer.errors, status=400)    
    # def get_parser_classes(self):
    #     if type(self.request.data)==dict:
    #         return [JSONParser]
    #     return [MultiPartParser]



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

