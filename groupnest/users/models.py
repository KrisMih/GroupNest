from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank = True)
    profile_picture = models.imageField(upload_to='/profile_pictures/', blank = True, null = True)
    rank = models.CharField(max_length = 50, default = "Newbie")

def str(self):
    return self.user.username