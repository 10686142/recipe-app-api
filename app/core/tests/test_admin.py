from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    # This build in function is ran before ANY test actually started,
    # so we can literally do the "setup" for our tests
    def setUp(self):
        """Sets up both users required for the testing methods"""
        # The test client that has helpfull methods like "force_login"
        self.client = Client()

        # Create the superuser
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@vazkirtest.nl',
            password='password123'
        )
        # It uses the Client helper function that helps you login with using,
        # Django's authentication, making it a lot easier compared to manual login
        self.client.force_login(self.admin_user)

        # Create the regular user
        self.user = get_user_model().objects.create_user(
            email='test@vazkirtest.nl',
            password='password123',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Test that are users are listed on user page"""
        # Generate the url our list users page
        # The reverse just grabs the url belonging to this key
        url = reverse('admin:core_user_changelist')

        # Performs a http GET on the url
        response = self.client.get(url)

        # Checks is the response object cotains certain items
        # in the content element of the the response object and also
        # checks that the HTTP response was 200 in thoses elements
        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_create_user_page(self):
        """Test that the create user page works"""
        # Generate the url our list users page
        # The reverse just grabs the url belonging to this key with id (edit page)
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        # Check if the page exists
        self.assertEqual(response.status_code, 200)


    def test_change_page(self):
        """Test that the user edit page works"""
        # Generate the url our list users page
        # The reverse just grabs the url belonging to this key with id (edit page)
        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        # Check if the page exists
        self.assertEqual(response.status_code, 200)
