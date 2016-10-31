"""
# Pages Controller Test

To run individually:

    nosetests -c nose.cfg tests/controllers/test_pages_controller.py
"""
import json

from controllers.pages import app as pages_controller

from tests.helper import (AppEngineControllerTest, MockIdentityService, XHR_HEADERS,
                          parse_html)


class PagesControllerTest(AppEngineControllerTest):
    #
    # Tests
    #
    def test_expects_to_get_home_page(self):
        # Arrange
        client = pages_controller.test_client()

        # Assume
        endpoint = '/'
        content_selector = 'div#home'

        # Act
        response = client.get(endpoint, follow_redirects=False)
        html = parse_html(response.data)
        content = html.select_one(content_selector) if html else None

        # Assert
        self.assertEqual(response.status_code, 200, html)
        self.assertIsNotNone(content)

    def test_expects_to_get_admin_page(self):
        # Arrange
        client = pages_controller.test_client()
        MockIdentityService.stub_app_engine_user(self, as_admin=True)

        # Assume
        endpoint = '/admin/'
        content_selector = 'div#admin'

        # Act
        response = client.get(endpoint, follow_redirects=False)
        html = parse_html(response.data)
        content = html.select_one(content_selector) if html else None

        # Assert
        self.assertEqual(response.status_code, 200, html)
        self.assertIsNotNone(content)

    def test_expects_to_get_ping_api_endpoint(self):
        # Arrange
        client = pages_controller.test_client()

        # Assume
        endpoint = '/api/ping/'

        # Act
        response = client.get(endpoint, headers=XHR_HEADERS, follow_redirects=False)
        json_data = json.loads(response.data)

        # Assert
        self.assertEqual(response.status_code, 200, json_data)
        self.assertEqual(json_data['ping'], 'pong')
