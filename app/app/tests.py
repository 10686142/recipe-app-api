# This is a class that comes with Django that basically has,
# a lot of helper functions that help is test our Django code
from django.test import TestCase


# Actual function to test
from app.calc import add, subsctract


class CaclTest(TestCase):

    # Any testable method needs to start with "test"
    def test_add_number(self):
        """Test that two numbers are added together"""
        self.assertEqual(add(2, 3), 5)

    def test_substract_number(self):
        """Test that values are substracted and returned"""
        self.assertEqual(subsctract(5, 11), 6)
