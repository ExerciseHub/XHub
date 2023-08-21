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