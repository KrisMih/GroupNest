from django.urls import path
from .views import LikeCreateView, LikeDestroyView, LikeListView

urlpatterns = [
    path('likes/<int:post_id>/likes/', LikeCreateView.as_view(), name='like-create-view'),
    path('likes/<int:pk>/delike/', LikeDestroyView.as_view(), name='like-destroy-view'),
    path('likes/<int:post_id>/likes/list/', LikeListView.as_view(), name='like-list-view'),
]
