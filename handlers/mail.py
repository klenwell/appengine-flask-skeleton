"""
# Inbound Mail Handler

Source
- https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/standard/mail/handle_incoming_email.py
"""
import logging
import webapp2

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler


class HipFlaskMailAuthorizationError(Exception): pass


class HipFlaskMailHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Message to %s from %s with subject: %s" % (mail_message.to,
                                                                 mail_message.sender,
                                                                 mail_message.subject))


app = webapp2.WSGIApplication([HipFlaskMailHandler.mapping()], debug=True)
