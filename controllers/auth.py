"""
# Auth Controller

Login/logout users.
"""
from google.appengine.api import users

from controllers import app, request, g, flash, redirect, session
from services import guest_service


@app.route('/login/', methods=['GET'])
def auth_login(origin=None):
    guest_service.check_guest_out(g.uest)
    return redirect(users.create_login_url(request.referrer))

@app.route('/logout/', methods=['GET'])
def auth_logout():
    guest_service.check_guest_out(g.uest)
    flash('You have been logged out.', 'success')
    return redirect(users.create_logout_url('/'))
