from django.http import Http404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
)
from .models import (
    User,
    DMRoom,
    DirectMessage
)
from .serializers import (
    UserSerializer,
    LoginSerializer,
    UserUpdateSerializer,
    MessageSerializer,
    RoomSerializer,
)


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
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'id'

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


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'nickname']


class FriendListView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'nickname']

    def get_queryset(self):
        user = self.request.user
        return user.friend.all()


class AddFriendView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        friend_id = request.data.get('friend_id')

        if not friend_id:
            return Response({"error": "friend_id 필드는 필수입니다."})
        
        try:
            friend = User.objects.get(id=friend_id)
        except User.DoesNotExist:
            return Response({"error": "해당 ID의 사용자를 찾을 수 없습니다."})
        
        if friend == request.user:
            return Response({"error": "자신을 친구로 추가할 수 없습니다."})
        
        request.user.friend.add(friend)

        if friend.nickname:
            return Response({"message": f"{friend.nickname}님이 친구 목록에 추가되었습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"{friend.email}님이 친구 목록에 추가되었습니다."}, status=status.HTTP_201_CREATED)


class RemoveFriendView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = 'friend_id'
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        friend_id = self.kwargs['friend_id']

        try:
            friend = User.objects.get(id=friend_id)
        except User.DoesNotExist:
            return Response({"error": "해당 ID의 사용자를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        if friend == request.user:
            return Response({"error": "자신을  친구 목록에서 제거할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if friend not in request.user.friend.all():
            return Response({"error": f"{friend.nickname if friend.nickname else friend.email}님은 이미 친구 목록에 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.friend.remove(friend)

        return Response({"message": f"{friend.nickname if friend.nickname else friend.email}님이 친구 목록에서 제거되었습니다."}, status=status.HTTP_204_NO_CONTENT)


### chat
class MessageListView(ListAPIView):
    queryset = DirectMessage.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return DirectMessage.objects.filter(room_id=room_id)


class CreateRoomView(CreateAPIView):
    queryset = DMRoom.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # 두 사용자의 ID를 받아옵니다. 
        user1 = request.user.id
        user2 = request.data.get("partner_id")

        # 유효성 검사: 파트너 사용자가 실제로 존재하는지 확인합니다.
        if not User.objects.filter(id=user2).exists():
            raise Http404("지정된 파트너 사용자가 존재하지 않습니다.")

        # 방 이름을 생성합니다. 항상 작은 숫자가 앞에 오도록 합니다.
        room_name = f"{min(user1, user2)}/{max(user1, user2)}"

        # 해당 이름의 방이 이미 존재하는지 확인하고, 있다면 기존 방을 반환합니다.
        room, created = DMRoom.objects.get_or_create(name=room_name, defaults={"host": request.user})

        if created:
            return Response({"message": "채팅방 생성!", "room_id": room.id}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "이미 존재하는 채팅방입니다.", "room_id": room.id}, status=status.HTTP_200_OK)
