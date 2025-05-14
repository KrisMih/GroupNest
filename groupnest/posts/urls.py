from django.urls import path
from .views import PostListCreateView, PostListDestroyView, PostList

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),  
    path('posts/<int:group_id>/', PostList.as_view(), name='post-list'),  
    path('posts/<int:pk>/delete/', PostListDestroyView.as_view(), name='post-delete'), 
]
