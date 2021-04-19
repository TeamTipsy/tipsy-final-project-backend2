from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('venues/', views.VenueList.as_view(), name='venue-list'),
    path('venues/<int:pk>/', views.VenueDetail.as_view(), name='venue-detail'),
]


urlpatterns += format_suffix_patterns(urlpatterns)