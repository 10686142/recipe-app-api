from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="test@vazkirrrr.com", password="testpass"):
    """Create sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@VazkIR.COM',
            'test123'
        )

        # Both need to be true as superuser
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@vazkir.com'
        password = 'PasswordTest123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # Make sure the email saved for the new user has been set correctly
        self.assertEqual(user.email, email)

        # The check_password method is a build in User method from Django that basically,
        # checks if given password is the one beloning to the user it's called on
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if the email for a new user is normalized"""
        email = 'test@VazkIR.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        # Check if it's lowercased
        self.assertEqual(user.email, email.lower())

    # Make sure we raise an error when no email address is provided
    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""

        # The "with" means that anything in there needs to raise the ValueError,
        # else meaning that this test will fail.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    # Make sure the str reperensentation is the acutal model.name
    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )

        self.assertEqual(str(tag), tag.name)

    # Test that our model is converted correltly into a string representation
    def test_ingredient_str(self):
        """Test ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Cucumber"
        )

        self.assertEqual(str(ingredient), ingredient.name)

    # Test that our model is converted correltly into a string representation
    def test_recipe_str(self):
        """Test recipe string representation"""
        # All the mandatory fields
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title="Steak and mushroom sauce",
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
