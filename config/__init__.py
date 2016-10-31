# Configuration Settings
import os
from config import secrets


# Set deployment stage: production (default), development, or test
if os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
    DEPLOYMENT_STAGE = 'development'
elif os.environ.get('SERVER_SOFTWARE', '') == 'TEST':
    DEPLOYMENT_STAGE = 'test'
else:
    DEPLOYMENT_STAGE = 'production'

PROJECT_NAME = 'Flask Gin (as set in config.__init__.py)'
