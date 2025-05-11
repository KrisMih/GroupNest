from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.GroupListCreateView.as_view(), name='group-list-create'),  
    path('groups/<int:pk>/', views.GroupDetailView.as_view(), name='group-detail'),  
    path('groups/<int:pk>/add_member/', views.AddMemberView.as_view(), name='add-member'), 
    path('groups/<int:pk>/remove_member/', views.RemoveMemberView.as_view(), name='remove-member'),
]
