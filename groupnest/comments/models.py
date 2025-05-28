from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name = 'comments', on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
