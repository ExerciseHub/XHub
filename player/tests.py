from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        # 유효한 회원 가입 데이터 생성
        data = {
            "email": "test@example.com",
            "password": "test",
            "nickname": "testuser",
            # "profile_image": "test.jpg",
            # "age": "2023-01-01"
        }
        # 회원 가입 API 엔드포인트 호출
        response = self.client.post(reverse("player:register"), data)
        # 응답 상태코드와 생성된 사용자 수 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        # 생성된 사용자의 이메일 주소 확인
        self.assertEqual(User.objects.get().email, "test@example.com")
    
    def test_registration_with_invalid_data(self):
        # 유효하지 않은 회원 가입 데이터 생성 (test case: 주요 항목 누락된 경우 발동)
        data = {
            "email": "test@example.com",
        }
        # 회원 가입 API 엔드포인트 호출
        response = self.client.post(reverse("player:register"), data)
        # 응답 상태코드 확인 (400 Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class UnregisterTestCase(APITestCase):
#     def setUp(self):
#         # 테스트에 사용할 사용자 생성
#         self.user = User.objects.create_user(
#             email="test@example.com", password="test", nickname="testuser"
#         )

#     def test_unregister(self):
#         # 생성한 사용자로 인증된 클라이언트 생성
#         self.client.force_authenticate(user=self.user)
#         # 회원 탈퇴 API 엔드포인트 호출
#         response = self.client.delete(reverse("player:unregister"))
#         # 응답 상태코드 확인 (204 No Content)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         # 사용자 삭제 여부 확인
#         self.assertEqual(User.objects.count(), 0)