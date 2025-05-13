from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.GroupListCreateView.as_view(), name='group-list-create'),  
    path('groups/<int:pk>/', views.GroupDetailView.as_view(), name='group-detail'),  
    path('groups/<int:pk>/add_member/', views.AddMemberView.as_view(), name='add-member'), 
    path('groups/<int:pk>/remove_member/', views.RemoveMemberView.as_view(), name='remove-member'),
    path('groups/<int:pk>/join/', views.JoinGroupView.as_view(), name='join-group'),
    path('groups/<int:pk>/leave/', views.LeaveGroupView.as_view(), name='leave-group'),
    path('groups/<int:pk>/accept/', views.AcceptJoinRequestView.as_view(), name='accept-request'),
    path('groups/<int:pk>/reject/', views.RejectJoinRequestView.as_view(), name='reject-request'),
]

