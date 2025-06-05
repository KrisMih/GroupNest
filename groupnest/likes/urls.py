from django.urls import path
from .views import LikeCreateView, LikeDestroyView

urlpatterns = [
    path('likes/<int:post_id>/likes/', LikeCreateView.as_view(), name='like-create-view'),
    path('likes/<int:pk>/dislike/', LikeDestroyView.as_view(), name='like-destroy-view'),
]
