from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
# from .views import Upload, VenueUpload, PostUpload

app_name='tipsyapp'

urlpatterns = [
    path('checkins/', views.CheckInList.as_view(), name='user-list'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<uuid:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('venues/', views.VenueList.as_view(), name='venue-list'),
    path('venues/<uuid:pk>/', views.VenueDetail.as_view(), name='venue-detail'),
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<uuid:pk>/', views.PostDetail.as_view(), name='post-detail'),
    # path('upload/', Upload.as_view(), name='upload'),
    # path('venueupload/', VenueUpload.as_view(), name='venue-upload'),
    # path('postupload/', PostUpload.as_view(), name='post-upload'),

]


urlpatterns += format_suffix_patterns(urlpatterns)
