from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Probar la api de usuarios"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Probar la creación de usuarios con el payload"""
        payload = {
            'email': 'user@example.com',
            'password': '_test@A123',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Probando que no se puede crear un usuario que ya existe"""
        payload = {
            'email': 'user@example.com',
            'password': '_test@A123',
            'name': 'Test name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Probar la contraseña debe ser mayor a 5 caracteres"""
        payload = {
            'email': 'user@example.com',
            'password': '1234',
            'name': 'Test password'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Probar que retorne el token para un usuario"""
        payload = {
            'email': 'user@example.com',
            'password': '_test@A123',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Probar que no retorne token si las credenciales son incorrectas"""
        create_user(email='user@example.com', password='test123@_')
        payload = {
            'email': 'user@example.com',
            'password': '_test@A123',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Probar que no retorne token cuando no existe el usuario"""
        payload = {
            'email': 'user@example.com',
            'password': '_test@A123',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_password(self):
        """Probar que no retorne token si hace falta la contraseña"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_email(self):
        """Probar que no retorne token si hace falta la contraseña"""
        res = self.client.post(TOKEN_URL, {'email': '', 'password': '_test@A'})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
