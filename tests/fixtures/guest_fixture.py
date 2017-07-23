"""
# Guest Model Fixture
"""
from models.guest import Guest

DEFAULT = {
    'auth_service'      : 'ip_address',
    'auth_service_id'   : '0.0.0.0'
}


def guest(**options):
    put = options.get('put', True)
    auth_service = options.get('auth_service', DEFAULT['auth_service'])
    auth_service_id = options.get('auth_service_id', DEFAULT['auth_service_id'])
    auth_service_name = options.get('auth_service_name')
    email = options.get('email')

    guest = Guest(auth_service      = auth_service,
                  auth_service_id   = auth_service_id,
                  auth_service_name = auth_service_name,
                  email             = email)

    if put:
        guest.put()

    return guest
