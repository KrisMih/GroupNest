from django.urls import path
from .views import PostListCreateView, PostListDestroyView, PostUpdateView, PostListView

urlpatterns = [
    path('posts/<int:group_id>/', PostListCreateView.as_view(), name='post-list-create'),  
    path('post/<int:pk>/', PostListView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-edit'), 
    path('posts/<int:pk>/delete/', PostListDestroyView.as_view(), name='post-delete'), 
]
