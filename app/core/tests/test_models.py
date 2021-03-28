from django.test import TestCase
from django.contrib.auth import get_user_model


class TestModel(TestCase):

    def test_create_user_with_email_succeeds(self):
        """Verificar la creación de un usuario con un email y contraseña"""
        email = 'test@example.com'
        password = '_TestPassword@123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Verificar que el correo de usuario este normalizado"""
        email = 'test@ExamplE.COM'
        user = get_user_model().objects.create_user(email, '_TestPassword')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Si se intenta crear un usuario sin correo, generar un error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '_TestPassword')

    def test_create_superuser(self):
        """Verificar la creación de un super usuario"""
        user = get_user_model().objects.create_superuser(
            'superuser@example.com',
            '_TestPassword@123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
