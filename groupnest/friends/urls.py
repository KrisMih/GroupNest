from django.urls import path
from .views import FriendRequestCreateView, FriendRequestListView, FriendRequestAcceptView, FriendRequestDeleteView, FriendListView


urlpatterns = [
    path('requests/', FriendRequestListView.as_view(), name='friend-request-list'),
    path('requests/send/', FriendRequestCreateView.as_view(), name='friend-request-create'),
    path('friends/', FriendListView.as_view(), name='friend-list'),
    path('requests/<int:pk>/accept/', FriendRequestAcceptView.as_view(), name='friend-request-accept'),
    path('requests/<int:pk>/delete/', FriendRequestDeleteView.as_view(), name='friend-request-delete'),
]