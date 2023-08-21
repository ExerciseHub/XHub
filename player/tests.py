from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            "email": "test@example.com",
            "password": "test",
            "nickname": "testuser",
            # "profile_image": "test.jpg",
            # "age": "2023-01-01"
        }
        response = self.client.post(reverse("player:register"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, "test@example.com")
    
    def test_registration_with_invalid_data(self):
        data = {
            "email": "test@example.com",
        }
        response = self.client.post(reverse("player:register"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UnregisterTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="", password="test", nickname="testuser"
        )

    def test_unregister(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("player:unregister"))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
