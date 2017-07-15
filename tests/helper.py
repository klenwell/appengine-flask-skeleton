"""
    Test Helper
"""
from unittest import TestCase
from unittest import skip   # As convenience for test modules.
from os.path import abspath, dirname, join
import hashlib
import email
from bs4 import BeautifulSoup
from urlparse import urlparse

from google.appengine.ext import ndb, testbed

from controllers import app
import config


#
# Constants
#
# See http://stackoverflow.com/a/9065860/1093087
XHR_HEADERS = [('X-Requested-With', 'XMLHttpRequest')]


#
# Base Test Classes
#
class AppEngineTestCase(TestCase):
    """Basic test case setup. This doesn't provide any patches or optimizations.
    It can be used as a baseline for comparing other base classes below.
    """
    def setUp(self, **options):
        app.config['TESTING'] = True
        self.longMessage = True
        self.testbed = make_bed(**options)

        # Optional mock csrf token: Default = True
        # WTF_CSRF_ENABLED: circumvents WTForm CSRF protection
        # ACCEPT_MOCK_CSRF_TOKEN: circumvents check_csrf filter
        if options.get('mock_csrf_token', True):
            app.config['WTF_CSRF_ENABLED'] = False
            app.config['ACCEPT_MOCK_CSRF_TOKEN'] = True

    def tearDown(self):
        self.testbed.deactivate()

    def initTaskQueueStub(self):
        self.testbed.init_taskqueue_stub(root_path=project_root())
        self.taskqueue_stub = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)

    def initMailStub(self):
        self.testbed.init_mail_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)
        return self.mail_stub

class AppEngineModelTest(AppEngineTestCase):
    """Using this class with counter patch speeds up test. See models/test_prediction.py
    for example of usage.
    """
    def setUp(self, **options):
        self.longMessage = True
        self.testbed = make_bed(**options)
        super(AppEngineModelTest, self).setUp(**options)

    def tearDown(self):
        self.testbed.deactivate()

class AppEngineControllerTest(AppEngineModelTest):
    """Similar to Model test except it inits user stub by default.
    """
    def setUp(self, **options):
        options['init_user_stub'] = options.get('init_user_stub', True)
        options['init_taskqueue_stub'] = options.get('init_taskqueue_stub', True)
        super(AppEngineControllerTest, self).setUp(**options)


def make_bed(**options):
    # Initializing the datastore stub with root_path enables tests to generate
    # index.yaml file. See http://stackoverflow.com/q/24702001/1093087.
    bed = testbed.Testbed()
    bed.activate()
    bed.init_datastore_v3_stub(root_path=project_root())
    bed.init_memcache_stub()

    # Optional user stub setup: Default = False. Note: MockIdentityService will
    # stub this.
    if options.get('init_user_stub'):
        bed.init_user_stub()

    # Optional task queue setup: Default = False
    if options.get('init_taskqueue_stub', False):
        bed.init_taskqueue_stub(root_path=project_root())
        bed.taskqueue_stub = bed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)

    # Optional mail stub setup: Default = False
    if options.get('init_mail_stub', False):
        bed.init_mail_stub()
        bed.mail_stub = bed.get_stub(testbed.MAIL_SERVICE_NAME)

    # Clear cache
    ndb.get_context().clear_cache()

    return bed


#
# Helper Methods
#
project_root = lambda: abspath(join(dirname(__file__), '..'))

def parse_html(markup):
    # Returns
    html = BeautifulSoup(markup, 'html.parser')
    return html

def redirect_path(response):
    if not response.location:
        return None
    else:
        return urlparse(response.location).path

def extract_id_from_url(url):
    if url is None:
        return None
    else:
        return int(re.search('\d+', url).group())


#
# Helper Classes and Fixtures
#
class MockIdentityService(object):

    @staticmethod
    def init_app_engine_user_service(test):
        """For tests that may not require a user but still need the service to
        be active.
        """
        test.testbed.init_user_stub()

    @staticmethod
    def stub_app_engine_user(test, **options):
        """Stubs App Engine user service.
        """
        email = options.get('email', 'user@gmail.com')
        user_id = hashlib.md5(email).hexdigest()
        is_admin = str(int(options.get('is_admin', False)))

        test.testbed.setup_env(USER_EMAIL=email,
                               USER_ID=user_id,
                               USER_IS_ADMIN=is_admin,
                               overwrite=True)
        test.testbed.init_user_stub()
        return user_id

    @staticmethod
    def login_app_engine_user(test, **options):
        options['email'] = options.get('email', 'guest@gmail.com')
        user_id = MockIdentityService.stub_app_engine_user(test, **options)
        return guests_fixture.app_engine_guest(**options)

    @staticmethod
    def login_app_engine_admin(test, **options):
        options['email'] = options.get('email', 'admin@gmail.com')
        options['is_admin'] = True
        options['auth_service_name'] = 'admin'
        options['auth_service_id'] = MockIdentityService.stub_app_engine_user(test, **options)
        return guests_fixture.app_engine_guest(**options)
