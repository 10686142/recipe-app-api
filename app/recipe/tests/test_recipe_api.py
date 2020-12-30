from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer

# We're using a viewset for the tag api endpoint, which means
# that we can specify which viewset we want with the "-"
RECIPES_URL = reverse('recipe:recipe-list')


# Test sample recipes we can use in our tests
def sample_recipe(user, **params):
    """Create and return a sample recipe"""

    # Default values to use for easier recipe creation
    # But can be overrided based on given params
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 10.0
    }

    # The update function will matc new k-v pairs to override
    # Or add newer ones if the params has new values
    defaults.update(params)

    # The assterixes pass the k-v to the creation of the model
    return Recipe.objects.create(user=user, **defaults)


class PublicRecipesApiTest(TestCase):
    """Test the publicly available recipes API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that the login is required for retrieving recipes"""
        response = self.client.get(RECIPES_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipesApiTest(TestCase):
    """Test the private Recipe API"""

    def setUp(self):
        """Setup the api client and authenticated user to list ingredients"""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@vazkir.com',
            password='PasswordTest123'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes_list(self):
        """Test retrieving a list of recipe"""
        # Create the ingredients to list for current user
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        response = self.client.get(RECIPES_URL)

        # Order reversed
        recipes = Recipe.objects.all().order_by('-id')

        # Serialzes the ingredients and thereby also manages the ordering
        # many=true indicates that we're dealing with many objects
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure the lists from the serializer and we added are the same,
        # so same items and same reversed ordering
        self.assertEqual(response.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test that recipes returned are for current authenticated user"""
        # Create a new user so we can assign a ingredient it, which should
        # not be part of the returned tags from this class's User
        other_user = get_user_model().objects.create_user(
            email='other_user@vazkir.com',
            password='PasswordTest123'
        )
        # Create sample recipes for our default and new user
        # So we can make sure only the new one is listed
        sample_recipe(user=other_user)
        sample_recipe(user=self.user)

        # Get the list url to use to compare to what we created
        response = self.client.get(RECIPES_URL)

        # Get default user owned recipe
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)
