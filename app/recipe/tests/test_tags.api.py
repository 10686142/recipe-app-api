from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer

# We're using a viewset for the tag api endpoint, which means
# that we can specify which viewset we want with the "-"
TAGS_URL = reverse('recipe:tag-list')


class PrivaeTagsApiTest(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        """Setup the api client and authenticated user to list tags"""
        self.user = get_user_model().objects.create_user(
            email='test@vazkir.com',
            password='PasswordTest123'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        )
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        response = self.client.post(TAGS_URL, payload)

        # Make sure this isn't actually added
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        # Create the tags to list for current user
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        response = self.client.get(TAGS_URL)

        # Order reversed alphabetically
        tags = Tag.objects.all().order_by('-name')

        # Serialzes the tags and thereby also manages the ordering
        # many=true indicates that we're dealing with many objects
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Make sure the lists from the serializer and we added are the same,
        # so same items and same reversed ordering
        self.assertEqual(response.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for current authenticated user"""
        # Create a new user so we can assign a tag it, which should
        # not be part of the returned tags from this class's User
        other_user = get_user_model().objects.create_user(
            email='other_user@vazkir.com',
            password='PasswordTest123'
        )
        # Add tag to other user
        Tag.objects.create(user=other_user, name="Fruity")

        # Add a tag to the authenticated user to make sure only the new one is listed
        new_tag = Tag.objects.create(user=self.user, name="Comfort Food")

        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], new_tag.name)


class PublicTagsApiTest(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that the login is required for retrieving tags"""
        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
