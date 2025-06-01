from django.db import models
from django.contrib.auth import get_user_model
from posts.models import  Post

User = get_user_model

class Like(models.model):
    user = models.ForeignKey(User, on_delet = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'likes')
    
    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
