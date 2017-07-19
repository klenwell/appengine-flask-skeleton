"""
# GuestRequest Model Fixture
"""
from models.guest_request import GuestRequest


def guest_request(**options):
    put = options.get('put', True)
    url = options.get('url', 'http://test-host/test/')
    path = options.get('path', '/test/')
    method = options.get('method', 'GET')
    ip_address = options.get('ip_address', '?.?.?.?')
    user_agent = options.get('user_agent', 'Mozilla/5.0 MockAgent/1.0')
    endpoint = options.get('endpoint', 'test_endpoint')
    referrer = options.get('referrer', 'http://referrer-host/referrer')

    guest_request = GuestRequest(guest_key      = None,
                                 session_id     = None,
                                 url            = url,
                                 path           = path,
                                 method         = method,
                                 ip_address     = ip_address,
                                 user_agent     = user_agent,
                                 endpoint       = endpoint,
                                 referrer       = referrer)

    if put:
        guest_request.put()

    return guest_request
