"""
# Guest Model

This model represents site visitors.

## Related Models

- has_many GuestRequests

"""
from google.appengine.ext import ndb
from google.appengine.api import memcache, users

import config


#
# Constants
#
AUTH_SERVICES = [
    'ip_address',
    'app_engine'
]

#
# Model
#
class Guest(ndb.Model):
    #
    # Attrs
    #
    # Fields
    auth_service                    = ndb.StringProperty(required=True, choices=AUTH_SERVICES)
    auth_service_id                 = ndb.StringProperty(required=True)
    auth_service_name               = ndb.StringProperty(required=False)
    email                           = ndb.StringProperty(required=False)

    # Count Fields
    total_requests                  = ndb.IntegerProperty(default=0)

    # Timestamps
    created_at                      = ndb.DateTimeProperty(auto_now_add=True)
    updated_at                      = ndb.DateTimeProperty(auto_now=True)

    #
    # Virtual Attrs
    #
    @property
    def unique_id(self):
        if not self.key:
            return None
        else:
            return self.key.id()

    @property
    def public_id(self):
        """Alias of unique_id."""
        if self.unique_id:
            return str(self.unique_id)[-8:]

    @property
    def public_name(self):
        if self.auth_service_name:
            return self.auth_service_name
        elif self.email:
            return self.email.split('@')[0]
        else:
            return 'Anonymous %s' % (str(self.public_id))

    @property
    def normalized_email(self):
        if not self.email:
            return None

        name, domain = self.email.split('@')
        name = name.replace('.', '').lower()
        return '%s@%s' % (name, domain.lower())

    #
    # Class Methods
    #
    # Find or Create Methods ###################################################
    @staticmethod
    def ip_address(ip_address):
        guest = Guest.query(Guest.auth_service == 'ip_address',
                            Guest.auth_service_id == ip_address).get()

        if guest:
            return guest
        else:
            return Guest.create(auth_service = 'ip_address',
                                auth_service_id = ip_address)

    @staticmethod
    def app_engine_user(app_engine_user):
        """App Engine User object docs:
        https://cloud.google.com/appengine/docs/standard/python/refdocs/google.appengine.api.users
        """
        user_id = app_engine_user.user_id()

        guest = Guest.query(Guest.auth_service == 'app_engine',
                            Guest.auth_service_id == user_id).get()

        if guest:
            return guest
        else:
            return Guest.create(auth_service = 'app_engine',
                                auth_service_id = user_id,
                                email = app_engine_user.email(),
                                auth_service_name = app_engine_user.nickname())


    # CRUD Methods #############################################################
    @staticmethod
    def create(**fields):
        guest = Guest(auth_service = fields.get('auth_service'),
                      auth_service_id = fields.get('auth_service_id'),
                      auth_service_name = fields.get('auth_service_name'),
                      email = fields.get('email'))

        guest.put()
        return guest

    @staticmethod
    def read(unique_id):
        return Guest._by_unique_id(unique_id)

    # Scope Methods ############################################################
    @staticmethod
    def s_recently_created(limit=100):
        return Guest.query().order(-Guest.created_at).fetch(limit)

    @staticmethod
    def get_by_email(email):
        return Guest.query(Guest.email == email).get()

    @staticmethod
    def _by_unique_id(unique_id):
        try:
            entity_id = int(unique_id)
            return ndb.Key('Guest', unique_id).get()
        except (TypeError, ValueError):
            return None

    #
    # Instance Methods
    #
    # Identifier / Role Methods
    def is_authenticated(self):
        valid_services = set(AUTH_SERVICES) - set(['ip_address'])
        return self.auth_service in valid_services

    def is_anonymous(self):
        return not self.is_authenticated()

    def is_admin(self):
        # Note: This can be modified to redefine admin based on app factors.
        return self.is_app_engine_admin()

    def is_app_engine_admin(self):
        return users.is_current_user_admin()
