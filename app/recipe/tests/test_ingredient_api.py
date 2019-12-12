from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTest(TestCase):
    """Test publicly available ingredient API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    """Test private ingredient API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            email="test@xyz.com",
            password="testpass"
        )
        self.client.force_authenticate(self.user)

    def test_retrive_ingredient_list(self):
        """Test retriving the list of ingredient"""
        Ingredient.objects.create(user=self.user, name="Apple")
        Ingredient.objects.create(user=self.user, name="Vinegar")
        res = self.client.get(INGREDIENT_URL)
        ingredient = Ingredient.objects.all().order_by('-name')

        # serializing the queryset into different form
        serializer = IngredientSerializer(ingredient, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that returned ingredient list is for autnehticated user only"""
        user2 = get_user_model().objects.create(
            email="some_user@xyz.com",
            password="aasdasds"
        )
        Ingredient.objects.create(user=user2, name="Someing")
        ingredient = Ingredient.objects.create(user=self.user, name="Vinegar")

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)

    def test_create_ingredients_succesfull(self):
        """Test creating ingredients"""
        payload = {
            'name': 'Cabbage'
        }
        res = self.client.post(INGREDIENT_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_ingredients_inalid(self):
        """Test creating invalid ingredients fails"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
