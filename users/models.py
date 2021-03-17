from django.db import models
from django.contrib.auth.models import User


class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    avatar = models.ImageField(upload_to='profile_images/', blank=True)

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return self.user.username


