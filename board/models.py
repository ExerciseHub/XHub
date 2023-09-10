from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


# Post 게시글 부분

class Post(models.Model):
    gather_title = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    context = models.TextField()
    img = models.ImageField(upload_to='images/post/', blank=True, null=True)
    like = models.PositiveIntegerField(default=0)
    public = models.BooleanField(default=True)  # 공개 여부
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.gather_title


# Comment 댓글 부분

class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    like = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def __str__(self):
        return self.content
