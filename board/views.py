from rest_framework.generics import CreateAPIView
from .models import Post
from .serializers import PostSerializers


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
