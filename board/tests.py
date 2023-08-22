# from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from player.models import User
from .models import Post


class PostCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", 
            password="testpassword"
        )
        self.client.login(
            email="testuser@example.com", 
            password="testpassword"
        )
        self.post_url  = '/board/write/'

    def test_create_post(self):
        post_data = {
            "title": "테스트 게시글 제목",
            "writer": self.user.email,
            "context": "테스트 게시글 내용",
            # "category": "축구(풋살)",
            # "location": "서울특별시 강남구",
            # "date": "2021-08-01",
            # "time": "18:00",
            # "number": 10,
        }

        response = self.client.post(self.post_url, post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_create_post_missing_data(self):
        post_data = {
            "title": "테스트 게시글 제목",
            "writer": self.user.email,
        }

        response = self.client.post(self.post_url, post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("context", response.data)

    def test_unauthenticated_post_creation(self):
        self.client.logout()

        post_data = {
            "title": "테스트 게시글 제목",
            "writer": self.user.email,
            "context": "테스트 게시글 내용",
        }

        response = self.client.post(self.post_url, post_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)