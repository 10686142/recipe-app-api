from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

# We're using a viewset for the tag api endpoint, which means
# that we can specify which viewset we want with the "-"
INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTest(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that the login is required for retrieving ingredients"""
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTest(TestCase):
    """Test the private ingredients API"""

    def setUp(self):
        """Setup the api client and authenticated user to list ingredients"""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@vazkir.com',
            password='PasswordTest123'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):
        """Test retrieving a list of ingredients"""
        # Create the ingredients to list for current user
        Ingredient.objects.create(user=self.user, name='Pepper')
        Ingredient.objects.create(user=self.user, name='Salt')

        response = self.client.get(INGREDIENTS_URL)

        # Order reversed alphabetically
        ingredients = Ingredient.objects.all().order_by('-name')

        # Serialzes the ingredients and thereby also manages the ordering
        # many=true indicates that we're dealing with many objects
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure the lists from the serializer and we added are the same,
        # so same items and same reversed ordering
        self.assertEqual(response.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that tags returned are for current authenticated user"""
        # Create a new user so we can assign a ingredient it, which should
        # not be part of the returned tags from this class's User
        other_user = get_user_model().objects.create_user(
            email='other_user@vazkir.com',
            password='PasswordTest123'
        )
        # Add ingredient to other user
        Ingredient.objects.create(user=other_user, name="Saltie")

        # Add a ingredient to the authenticated user to make sure only the new one is listed
        new_ingredient = Ingredient.objects.create(user=self.user, name="Sweet caramel")

        # Get the list url to use to compare to what we created
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], new_ingredient.name)

    def test_create_ingredient_successful(self):
        """Test creating a new ingredient"""
        payload = {'name': 'Test ingredient Saltie'}
        self.client.post(INGREDIENTS_URL, payload)

        # Try to find the model we just created by new and user
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test creating a new ingredient with invalid payload"""
        payload = {'name': ''}
        response = self.client.post(INGREDIENTS_URL, payload)

        # Make sure this isn't actually added
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
