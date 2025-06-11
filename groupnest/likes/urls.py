from django.urls import path
from .views import LikeCreateView, LikeDestroyView, LikeListView

urlpatterns = [
    path('post/<int:post_id>/like/', LikeCreateView.as_view(), name='like-create-view'),
    path('post/<int:post_id>/unlike/', LikeDestroyView.as_view(), name='like-destroy-view'),
    path('post/<int:post_id>/like/list/', LikeListView.as_view(), name='like-list-view'),
]
