"""
# Guest Requests Controller Test

To run individually:

    nosetests -c nose.cfg tests/controllers/test_guest_requests_controller.py
"""
import json

from controllers.guest_requests import app as guest_requests_controller

from tests.helper import (AppEngineControllerTest, parse_html)
from tests.fixtures import guest_request_fixture
from models.guest_request import GuestRequest


class GuestRequestsControllerTest(AppEngineControllerTest):
    #
    # Tests
    #
    def test_expects_index_to_list_recent_guest_requests(self):
        # Arrange
        client = guest_requests_controller.test_client()
        for n in range(5):
            guest_request_fixture.guest_request(put=True)

        # Assume
        endpoint = '/guest-requests/'
        row_selector = 'table.guest-requests > tbody > tr'
        self.assertEqual(GuestRequest.query().count(), 5)

        # Act
        response = client.get(endpoint, follow_redirects=False)
        html = parse_html(response.data)
        rows = html.select(row_selector) if html else None

        # Assert
        self.assertEqual(response.status_code, 200, html)
        self.assertEqual(len(rows), 6)
