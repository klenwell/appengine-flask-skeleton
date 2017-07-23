#
# Template
#
def active_tab_class(request, tab_path, **options):
    # Use request.path. request.url_rule.rule does not exist for errorhandler.
    request_path = request.path if request.path else ''

    if options.get('alt'):
        tab_paths = [tab_path] + options['alt']
    else:
        tab_paths = [tab_path]

    def is_exact_wildcard_match(path):
        path_crumbs = path.split('/')
        request_crumbs = request_path.split('/')

        for n, crumb in enumerate(path_crumbs):
            if crumb == '*':
                continue

            if crumb != request_crumbs[n]:
                return False

        return True

    for path in tab_paths:
        if options.get('endswith'):
            if request_path.endswith(path):
                return 'active'
        elif options.get('exact'):
            if '*' in path and is_exact_wildcard_match(path):
                return 'active'
            elif request_path == path:
                return 'active'
        else:
            if request_path.startswith(path):
                return 'active'

    return 'inactive'

def at(a_datetime):
    f = '%Y-%m-%d %H:%M:%S'

    if not a_datetime:
        return 'N/A'
    else:
        return a_datetime.strftime(f).lower()

def filter_flash_messages(messages, filter_by):
    unique_messages = []
    for category, message in messages:
        if category.startswith(filter_by) and message not in unique_messages:
            unique_messages.append(message)
    return unique_messages
