from django.urls import path
from .views import CommentListCreateView, CommentRetrieveUpdateDestroyView

urlpatterns = [
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name = 'comment-list-create'),
    path('comments/<int:pk>/deleteupdate/', CommentRetrieveUpdateDestroyView.as_view(), name = 'comment-retrieve-update-delete'),
]