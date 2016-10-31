"""
# Mail Handler Test

To run individually:

    nosetests -c nose.cfg tests/handlers/test_mail_handler.py
"""
from email.mime.text import MIMEText
from webtest import TestApp

from google.appengine.api.mail import InboundEmailMessage

from handlers.mail import app, HipFlaskMailAuthorizationError

from tests.helper import (AppEngineTestCase)


class InboundMailerTest(AppEngineTestCase):
    #
    # Tests
    #
    def test_expects_inbound_email_to_be_handled(self):
        # Arrange
        client = TestApp(app)
        mime_message = MIMEText('Hello world!')
        mime_message['Subject'] = 'Mailer Test'
        mime_message['From'] = 'sender@gmail.com'
        mime_message['To'] = 'test@test.appspotmail.com'
        mail_message = InboundEmailMessage(mime_message)

        # Assume
        endpoint = '/_ah/mail/test.appspotmail.com'
        body = mail_message.original.as_string()

        # Act
        response = client.post(endpoint, body)

        # Assert
        self.assertEqual(response.status_code, 200, response)
