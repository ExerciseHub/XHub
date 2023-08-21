from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import (
    UserSerializer,
    LoginSerializer,
    UserUpdateSerializer,
)
from .models import User


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 성공!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')

        refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(res, status=status.HTTP_200_OK)


class Logout(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        response = Response({"detail": "Logout Successful"}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh')
        response.delete_cookie('access')
        return response


class Update(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    # renderer_classes 보류
    serializer_class = UserUpdateSerializer

    def get(self, reuqest, *args, **kwargs):
        serializer = self.serializer_class(reuqest.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        serializer_data = request.data

        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UnregisterUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "회원탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)


# RegisterView = RegisterView.as_view()
# Login = Login.as_view()
# Logout = Logout.as_view()
# Update = Update.as_view()
# UnregisterUserView = UnregisterUserView.as_view()
