from rest_framework.test import APITestCase
from rest_framework import status
from player.models import User
from .models import Post


# 테스트 케이스 실행 전 초기 설정을 합니다.

class PostCreateTestCase(APITestCase):
    def setUp(self):

        # 테스트 유저를 생성하고 로그인합니다.

        self.user = User.objects.create_user(
            email="testuser@example.com", 
            password="testpassword"
        )
        self.client.login(
            email="testuser@example.com", 
            password="testpassword"
        )

        # 게시글 작성 URL을 설정합니다.

        self.post_url  = '/board/write/'

    # 게시글 생성 테스트를 수행합니다.

    def test_create_post(self):

        # 게시글 데이터를 생성합니다.

        post_data = {
            "gather-title": "테스트 게시글 제목",
            "writer": self.user.id, # 이메일 대신 user.id 로 수정
            "context": "테스트 게시글 내용",
            # "category": "축구(풋살)",
            # "location": "서울특별시 강남구",
            # "date": "2021-08-01",
            # "time": "18:00",
            # "number": 10,
        }

        # POST 요청을 보내 게시글을 생성하고 응답을 받습니다.

        response = self.client.post(self.post_url, post_data)
        # print(response.data) # 디버깅용

        # 응답 상태 코드와 데이터베이스 내 게시글 수를 확인합니다.

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    # 데이터 누락된 상태로 게시글 생성을 시도함으로서 기능을 검증합니다.

    def test_create_post_missing_data(self):
        post_data = {
            "gather-title": "테스트 게시글 제목",
            "writer": self.user.email,
        }

        response = self.client.post(self.post_url, post_data)

        # 응답 상태 코드를 확인하고 context 필드의 오류를 확인합니다.

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("context", response.data)

    # 인증되지 않은 유저의 게시글 생성 테스트를 수행합니다.

    def test_unauthenticated_post_creation(self):

        # 유저를 로그아웃시킵니다.

        self.client.logout()

        post_data = {
            "gather-title": "테스트 게시글 제목",
            "writer": self.user.email,
            "context": "테스트 게시글 내용",
        }

        response = self.client.post(self.post_url, post_data)

        # 응답 상태 코드를 확인합니다.

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)