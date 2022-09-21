from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.
# Create your models here.

class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    username = models.CharField(max_length=50,blank=True,null=True,unique=True)
    email = models.EmailField(unique=True)
    password =models.CharField(max_length=1000,blank=False,null=False)
    image =models.ImageField(upload_to='media/', blank=True)
    joined_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.username