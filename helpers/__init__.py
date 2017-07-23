from helpers import template_helpers
from helpers import string_helpers


# This will be used by Flask's @app.context_processor (in controllers.__init__)
api = dict(
    active_tab_class        = template_helpers.active_tab_class,
    at                      = template_helpers.at,
    filter_flash_messages   = template_helpers.filter_flash_messages,
    parameterize            = string_helpers.parameterize,
    pluralize               = string_helpers.pluralize
)
