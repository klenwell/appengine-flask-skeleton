"""
# Auth Controller Test

To run individually:

    nosetests -c nose.cfg tests/controllers/test_auth_controller.py
"""
import json

from flask import g

from tests.helper import (AppEngineControllerTest, MockIdentityService, XHR_HEADERS,
                          parse_html, redirect_path)
from tests.fixtures import guest_fixture
from controllers.auth import app as auth_controller
from models.guest import Guest


class PagesControllerTest(AppEngineControllerTest):
    #
    # Tests
    #
    def test_expects_to_get_login_page(self):
        # Arrange
        client = auth_controller.test_client()

        # Assume
        endpoint = '/login/'
        expected_redirect_url = 'https://www.google.com/accounts/Login?' + \
                                'continue=http%3A//testbed.example.com/'

        # Act
        response = client.get(endpoint, follow_redirects=False)

        # Assert
        self.assertEqual(response.status_code, 302, response.data)
        self.assertEqual(response.location, expected_redirect_url)

    def test_expects_to_log_out_guest(self):
        pass
