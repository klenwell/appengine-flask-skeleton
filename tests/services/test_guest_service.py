"""
# Guest Service Tests

To run individually:

    nosetests -c nose.cfg tests/services/test_guest_service.py
"""
from google.appengine.api import users

from services import guest_service
from models.guest import Guest

from tests.helper import (AppEngineTestCase, MockIdentityService)


#
# Test Case
#
class GuestServiceTest(AppEngineTestCase):
    #
    # Class Tests
    #
    def test_generate_session_id(self):
        # Arrange
        email = 'user@gmail.com'
        app_engine_user_id = MockIdentityService.stub_app_engine_user(self, email=email)
        app_engine_user = users.get_current_user()
        guest = Guest.app_engine_user(app_engine_user)

        # Act
        session_id = guest_service.generate_session_id(guest)

        # Assert
        self.assertIsNotNone(session_id)
