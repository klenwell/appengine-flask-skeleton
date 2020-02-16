"""
# Guests Controller Test

To run individually:

    nosetests -c nose.cfg tests/controllers/test_guests_controller.py
"""
import json

from controllers.guests import app as guests_controller

from tests.helper import (AppEngineControllerTest, parse_html)
from tests.fixtures import guest_fixture
from models.guest import Guest


class GuestsControllerTest(AppEngineControllerTest):
    #
    # Tests
    #
    def test_expects_to_get_index(self):
        # Arrange
        client = guests_controller.test_client()

        # Assume
        endpoint = '/guests/'
        row_selector = 'table.guests > tbody > tr'
        self.assertEqual(Guest.query().count(), 0)

        # Act: this will create new anonymous guest
        response = client.get(endpoint, follow_redirects=False)
        html = parse_html(response.data)
        rows = html.select(row_selector) if html else None

        # Assert
        self.assertEqual(response.status_code, 200, html)
        self.assertEqual(len(rows), 1, html)
