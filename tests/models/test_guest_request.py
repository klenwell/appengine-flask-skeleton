"""
# GuestRequest Model Tests

To run individually:

    nosetests -c nose.cfg tests/models/test_guest_request.py
"""
from google.appengine.api import users

from models.guest_request import GuestRequest

from tests.helper import (AppEngineModelTest, MockIdentityService, MockRequest)
from tests.fixtures import guest_fixture


#
# Test Case
#
class GuestRequestModelTest(AppEngineModelTest):
    #
    # Class Tests
    #
    def test_expects_to_create_new_guest_request(self):
        # Arrange
        ip_address = '127.0.0.1'
        session_id = 'mock-session-id'
        guest = guest_fixture.guest(auth_service='ip_address',
                                    auth_service_id=ip_address)
        request = MockRequest()

        # Act
        guest_request = GuestRequest.create(guest,
                                            request,
                                            ip_address=ip_address,
                                            session_id=session_id,
                                            session_counter=0)

        # Assert
        self.assertEqual(guest_request.session_id, session_id)
        self.assertEqual(guest_request.guest.unique_id, guest.unique_id)
        self.assertEqual(guest_request.user_agent, request.headers['User-Agent'])
