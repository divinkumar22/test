from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    unique_key  = models.CharField(max_length=100)


