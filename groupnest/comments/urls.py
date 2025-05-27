from django.urls import path
from .views import CommentListCreateView, CommentRetrieveUpdateDestroyView

urlpatterns = [
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name = CommentListCreateView),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name = CommentRetrieveUpdateDestroyView),
]