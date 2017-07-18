"""
# Pages Controller Test

To run individually:

    nosetests -c nose.cfg tests/controllers/test_pages_controller.py
"""
import json

from flask import g

from tests.helper import (AppEngineControllerTest, MockIdentityService, XHR_HEADERS,
                          parse_html)
from tests.fixtures import guest_fixture
from controllers.pages import app as pages_controller
from models.guest import Guest
from models.guest_request import GuestRequest


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

    def test_expects_admin_to_get_admin_page(self):
        # Arrange
        client = pages_controller.test_client()
        MockIdentityService.stub_app_engine_user(self, is_admin=True)

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

    def test_expects_guest_service_to_create_guest_for_first_time_visitor(self):
        # Arrange
        client = pages_controller.test_client()
        endpoint = '/'
        ip_address = '127.0.0.1'

        # Assume
        self.assertEqual(Guest.query().count(), 0)

        # Act
        response = client.get(endpoint,
                              follow_redirects=False,
                              environ_base={'REMOTE_ADDR': ip_address})
        new_guest = Guest.query().get()

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Guest.query().count(), 1)
        self.assertEqual(new_guest.auth_service, 'ip_address')
        self.assertEqual(new_guest.auth_service_id, ip_address)

    def test_expects_guest_service_to_find_guest_for_return_visitor(self):
        # Arrange
        client = pages_controller.test_client()
        endpoint = '/'
        ip_address = '127.0.0.1'
        guest = guest_fixture.guest(auth_service='ip_address',
                                    auth_service_id=ip_address)

        # Assume
        self.assertEqual(Guest.query().count(), 1)

        # g accessible when using client as context pattern:
        # http://flask.pocoo.org/docs/0.10/testing/#keeping-the-context-around
        with client as request_context:
            # Act
            response = request_context.get(endpoint,
                                           follow_redirects=False,
                                           environ_base={'REMOTE_ADDR': ip_address})

            # Assert
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Guest.query().count(), 1)
            self.assertIsNotNone(g.uest)
            self.assertEqual(g.uest.public_id, guest.public_id)
            self.assertEqual(guest.auth_service, 'ip_address')
            self.assertEqual(guest.auth_service_id, ip_address)

    def test_expects_guest_service_to_save_guest_requests(self):
        # Arrange
        client = pages_controller.test_client()

        # Assume
        endpoint = '/'
        self.assertEqual(Guest.query().count(), 0)
        self.assertEqual(GuestRequest.query().count(), 0)

        # Act
        response = client.get(endpoint,
                              follow_redirects=False,
                              environ_base={'REMOTE_ADDR': '127.0.0.1'})
        guest = Guest.query().get()
        guest_request = GuestRequest.query().get()

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Guest.query().count(), 1)
        self.assertEqual(GuestRequest.query().count(), 1)
        self.assertEqual(guest_request.guest.unique_id, guest.unique_id)
