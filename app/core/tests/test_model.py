from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
"""
Get User model: https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#django.contrib.auth.get_user_model
""" # noqa


def sample_user(email="test@surya.com", password="test123"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """Test the tage string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertAlmostEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
