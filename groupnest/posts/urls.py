from django.urls import path
from .views import PostListCreateView, PostListDestroyView, PostList

urlpatterns = [
    path('posts/<int:group_id>/', PostListCreateView.as_view(), name='post-list-create'),    
    path('posts/<int:pk>/delete/', PostListDestroyView.as_view(), name='post-delete'), 
]
