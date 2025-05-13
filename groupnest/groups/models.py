from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_groups')
    members = models.ManyToManyField(User, related_name='member_groups')
    is_private = models.BooleanField(default=False)
    join_requests = models.ManyToManyField(User, related_name='join_requests', blank=True)

    def __str__(self):
        return self.name

