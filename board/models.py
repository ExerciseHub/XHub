from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    context = models.TextField()
    img = models.ImageField(blank=True, null=True)
    like = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Modes):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    like = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
