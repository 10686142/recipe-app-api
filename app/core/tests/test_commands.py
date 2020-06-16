# Patch: Allows us to mock the behavior of the django_get_database function
# We can simulate the db being available or not available when running TestCommand methods
from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """What happens when we can our command and db is avaialble"""

        # Mock the connection to the db, by tring to retrieve the default db connection;
        # the "ConnectionHandler" with the __getitem__ retrieving the db
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # Override is by returning True, aka the mock object
            gi.return_value = True

            # Our custom command
            call_command('wait_for_db')

            # Makes sure it's only called once
            self.assertEqual(gi.call_count, 1)

    # So we're mocking the time.sleep function, so the function needs to an extra parameter
    # It just replaces the time.sleep function and replaces with with a funtion returning True
    # So during our tests it won't actually wait the second we supply it, to speed up the test
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        # Checks if the OperationalError is gone each second for 5 seconds, aka db is ready
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # We'r going to add a side effect to trigger the OperationalError the first 5 times
            gi.side_effect = [OperationalError] * 5 + [True]  # Create s side_effect list

            # Call the command
            call_command('wait_for_db')

            # Makes sure it's called 6 times since this would not yield the OperationalError
            self.assertEqual(gi.call_count, 6)
