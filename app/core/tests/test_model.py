from django.test import TestCase
from django.contrib.auth import get_user_model

"""
Get User model: https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#django.contrib.auth.get_user_model
""" # noqa


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is succesfull"""
        # setup an test  email and password
        email = 'test@surya.com'
        password = 'Testpass123'

        # execute
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        # check the test
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for new user is normalized"""
        """Normalize the email address by lowercasing the domain part of it."""
        email = 'test@SURYA.com'
        user = get_user_model().objects.create_user(email, 'test')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no emalil raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new super user."""
        user = get_user_model().objects.create_superuser(
            'test@SURYA.com',
            'test'
        )

        # superuser privilage is included in PermissionMixins Class
        self.assertTrue(user.is_superuser)
