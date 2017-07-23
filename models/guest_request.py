"""
# Guest Request

Guest request or page view.

## Related Models

- belongs_to Guest
"""
from google.appengine.ext import ndb


#
# Model
#
class GuestRequest(ndb.Model):
    #
    # Attrs
    #
    # Fields
    url                     = ndb.StringProperty(required=True)
    path                    = ndb.StringProperty(required=True)
    method                  = ndb.StringProperty(required=True)
    ip_address              = ndb.StringProperty(required=False)
    user_agent              = ndb.StringProperty(required=False)
    endpoint                = ndb.StringProperty(required=False)
    referrer                = ndb.StringProperty(required=False)
    session_id              = ndb.StringProperty(required=False)
    session_counter         = ndb.IntegerProperty(default=0)

    # Related Models
    guest_key               = ndb.KeyProperty(required=False)        # kind=Guest

    # Timestamps
    created_at              = ndb.DateTimeProperty(auto_now_add=True)
    updated_at              = ndb.DateTimeProperty(auto_now=True)

    #
    # Virtual Attrs
    #
    @property
    def public_id(self):
        if not self.key:
            return None
        else:
            return self.key.id()

    # Relationships
    @property
    def guest(self):
        if self.guest_key:
            return self.guest_key.get()
        else:
            return None

    @property
    def guest_id(self):
        if not self.guest:
            return None
        else:
            return self.guest.unique_id

    #
    # Class Methods
    #
    # CRUD Methods #############################################################
    @staticmethod
    def create(guest, request, **options):
        """Includes option to save only those requests with a valid endpoint.
        """
        ip_address = options.get('ip_address')
        session_id = options.get('session_id')
        session_counter = options.get('session_counter')
        require_endpoint = options.get('require_endpoint', True)

        guest_request = GuestRequest(guest_key = guest.key if guest else None,
                                     endpoint = request.endpoint,
                                     path = request.path,
                                     ip_address = ip_address,
                                     referrer = request.referrer,
                                     session_id = session_id,
                                     session_counter = session_counter,
                                     url = request.url,
                                     user_agent = request.headers.get('User-Agent'),
                                     method = request.method)

        if require_endpoint and guest_request.endpoint:
            guest_request.put()

        return guest_request

    @staticmethod
    def read(public_id):
        return GuestRequest._by_public_id(public_id)

    # Scope Methods ############################################################
    @staticmethod
    def s_recently_created(limit=100):
        return GuestRequest.query().order(-GuestRequest.created_at).fetch(limit)

    @staticmethod
    def _by_public_id(public_id):
        if not public_id:
            return None
        else:
            return ndb.Key('GuestRequest', public_id).get()

    #
    # Instance Methods
    #
