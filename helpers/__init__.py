from helpers import template_helpers


# This will be used by Flask's @app.context_processor (in controllers.__init__)
api = dict(
    active_tab_class    = template_helpers.active_tab_class
)
