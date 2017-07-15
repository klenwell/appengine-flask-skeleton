"""
# Guest Service

Services for guests.

Usage:

    from services import guest_service
    guest_service.check_guest_in()
"""
from time import time

from google.appengine.api import users
from flask import (request, session)

from models.guest import Guest


#
# Constants
#
SERVICE_KEY = 'guest-service'
TALLY_KEY = 'guest-service-tally'


#
# Service API
#
def check_guest_in():
    # Identify Guest.
    guest = identify_guest()

    # Get session ID.
    is_returning = SERVICE_KEY in session

    if is_returning:
        session[TALLY_KEY] += 1
    else:
        session[SERVICE_KEY] = generate_session_id(guest)
        session[TALLY_KEY] = 1

    # TODO: Log request.

    # Return Guest
    return guest

def check_guest_out(guest):
    if guest:
        guest = None
        session.pop(SERVICE_KEY, None)
        session.pop(TALLY_KEY, None)

#
# Internal Module Methods
#
def identify_guest():
    """Returns with an App Engine user or an anonymous user.
    """
    app_engine_user = users.get_current_user()

    if app_engine_user:
        return Guest.app_engine_user(app_engine_user)

    ip_address = ip_address_from_request(request)
    return Guest.ip_address(ip_address)

def generate_session_id(guest):
    micro_timestamp = int(round(time() * 100000))
    return '%s-%s' % (guest.public_id, micro_timestamp)

def ip_address_from_request(request):
    """Returns guest's IP address. This may be complicated by proxies.
    Source: https://stackoverflow.com/q/3759981/1093087"""
    # Source: https://stackoverflow.com/a/25040332/1093087
    remote_addr = request.environ.get('REMOTE_ADDR')

    if remote_addr:
        return remote_addr
    else:
        # Source: https://stackoverflow.com/a/26654607/1093087
        return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
