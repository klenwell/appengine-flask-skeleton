"""
# Guest Model Tests

To run individually:

    nosetests -c nose.cfg tests/models/test_guest.py
"""
from google.appengine.api import users

from models.guest import Guest

from tests.helper import (AppEngineModelTest, MockIdentityService)


#
# Test Case
#
class GuestModelTest(AppEngineModelTest):
    #
    # Class Tests
    #
    def test_expects_to_save_new_anonymous_guest(self):
        # Arrange
        auth_service = 'ip_address'
        auth_service_id = '127.0.0.1'

        # Act
        guest = Guest(auth_service = auth_service,
                      auth_service_id = auth_service_id)
        guest.put()

        # Assert
        self.assertIsInstance(guest, Guest)
        self.assertEqual(guest.auth_service, auth_service)
        self.assertIsNotNone(guest.key)

    def test_expects_to_create_new_anonymous_guest(self):
        # Arrange
        ip_address = '127.0.0.1'

        # Act
        guest = Guest.ip_address(ip_address)

        # Assert
        self.assertEqual(guest.auth_service, 'ip_address')
        self.assertEqual(guest.auth_service_id, ip_address)

    def test_expects_to_create_new_app_engine_guest(self):
        # Arrange
        email = 'user@gmail.com'
        app_engine_user_id = MockIdentityService.stub_app_engine_user(self, email=email)
        app_engine_user = users.get_current_user()

        # Assume
        self.assertEqual(app_engine_user.user_id(), app_engine_user_id)

        # Act
        guest = Guest.app_engine_user(app_engine_user)

        # Assert
        self.assertEqual(guest.auth_service, 'app_engine')
        self.assertEqual(guest.auth_service_id, app_engine_user_id)
