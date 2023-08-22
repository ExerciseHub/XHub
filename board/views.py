from rest_framework.generics import CreateAPIView
from .models import Post
from .serializers import PostSerializers
from rest_framework.permissions import IsAuthenticated


class PostCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializers
