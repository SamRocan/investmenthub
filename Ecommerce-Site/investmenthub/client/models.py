from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='client', on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profilepics/', default='profilepics/default.png')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name