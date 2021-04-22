from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('users/<uuid:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('venues/', views.VenueList.as_view(), name='venue-list'),
    path('venues/<uuid:pk>/', views.VenueDetail.as_view(), name='venue-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<uuid:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('venue_posts/', views.VenuePostList.as_view(), name='venue_post-list'),
    path('venue_posts/<uuid:pk>/', views.VenuePostDetail.as_view(), name='venue_post-detail'),
]


urlpatterns += format_suffix_patterns(urlpatterns)
