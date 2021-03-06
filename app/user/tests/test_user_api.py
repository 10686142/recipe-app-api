from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

# Makes status codes more readable
from rest_framework import status


# Constants used for this test
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


# The **param is a dynamic list of arguments, meaning
# we have a lot of flexibility of fields we can assign to users
# for the sample test users we're creating
def create_user(**params):
    return get_user_model().objects.create_user(**params)


# A "Private" api needs authentication compared to the "Public"
class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    # Sets up the APIClient
    def setUp(self):
        # The authenticated user, used in subsequent test methods
        self.user = create_user(
            email='test@vazkirauth.com',
            password='testpass',
            name='name'
        )
        # Initialize the API Client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        # Get my user info
        response = self.client.get(ME_URL)

        # Checks the API response code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # So no checking password since hashed.
        self.assertEqual(response.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the url"""
        response = self.client.post(ME_URL)

        # Make sure we get a not allowed back
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'password': 'newpass123', 'name': 'new_name'}

        # Make a PATCH to update an existing db row
        response = self.client.patch(ME_URL, payload)

        # Make sure the self.user is updated to the latest changes
        self.user.refresh_from_db()

        # And now we want to check if our name change went through
        self.assertEqual(self.user.name, payload['name'])

        # Also check the password change
        self.assertTrue(self.user.check_password(payload['password']))

        # Make sure the response was oke.
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# A "Public" api doesn't need authentication, so like creating a user
class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    # Sets up the APIClient
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_user_unauthorized(self):
        # Get my user info
        response = self.client.get(ME_URL)

        # Make sure the url for information about this user is not publicly accesible
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@mail.com', 'password': 'testpass'}

        # Use the "create_user" function we created to create it normally
        create_user(**payload)

        # Creates the POST request to get the token for user
        response = self.client.post(TOKEN_URL, payload)

        # Checks the API response code has a token
        self.assertIn('token', response.data)

        # Checks the API response code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created when invalid credentials are given"""
        payload = {'email': 'test@mail.com', 'password': 'testpass'}

        # Use the "create_user" function we created to create it normally
        create_user(**payload)

        # To test if passing wrong password will also give me an auth token
        payload_wrong_pass = {'email': 'test@mail.com', 'password': 'wrongpass'}

        # Creates the POST request to get the token for user,
        # but has the wrong password provided
        response = self.client.post(TOKEN_URL, payload_wrong_pass)

        # Checks the API response code has a token
        self.assertNotIn('token', response.data)

        # Checks the API response code is a bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@mail.com', 'password': 'testpass'}

        # IMPORTANT: So we're not creating the user first, so it should not work
        # Creates the POST request to get the token for user
        response = self.client.post(TOKEN_URL, payload)

        # Checks the API response code has a token
        self.assertNotIn('token', response.data)

        # Checks the API response code is a bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {'email': 'test@mail.com', 'password': ''}

        # Creates the POST request to get the token for user with no password
        response = self.client.post(TOKEN_URL, payload)

        # Checks the API response code has a token
        self.assertNotIn('token', response.data)

        # Checks the API response code is a bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {'email': 'shortpasstest@mail.com', 'password': 'pw', 'name': 'test'}

        # Creates the POST request to create the new user with the too short password
        response = self.client.post(CREATE_USER_URL, payload)

        # Checks the API response code is a bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Validate that the user did not get created
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        # Test if it's False or None
        self.assertFalse(user_exists)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'existingusertest@mail.com', 'password': 'testpass', 'name': 'test'}

        # Use the "create_user" function we created to create it normally
        create_user(**payload)

        # Creates the POST request to create the same user again through the API
        response = self.client.post(CREATE_USER_URL, payload)

        # Checks the API response code is a bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_valid_user_success(self):
        """Test creating user with valid payload successful"""
        payload = {
            'email': 'testpublicapi@mail.com',
            'password': 'testpass',
            'name': 'Test Name'
        }

        # Creates the POST request to create a new user
        response = self.client.post(CREATE_USER_URL, payload)

        # Checks the API response code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Takes the dict response.data and just passes it in as the parameters for;
        # the .get(), which should retrieve this new user successfully
        user = get_user_model().objects.get(**response.data)

        # Then validate if the returned user is the one we created via POST
        self.assertTrue(user.check_password(payload['password']))

        # Lastly make sure the actual passwork isn't returned in the request (security reasons)
        self.assertNotIn('password', response.data)
