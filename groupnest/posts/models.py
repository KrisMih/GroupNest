from django.db import models
from django.contrib.auth.models import User
from groups.models import Group

class Post(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title