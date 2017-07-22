"""
# Guests Controller
"""
from datetime import datetime, timedelta

from controllers import app, render_template, g
from models.guest import Guest


#
# Guests
#
@app.route('/guests/', methods=['GET'])
def guests_index():
    guests = Guest.s_recently_created(25)
    return render_template('guests/index.html',
                           guests=guests,
                           table='guests/_table.html')

@app.route('/admin/guests/', methods=['GET'])
def guests_admin_index():
    guests = Guest.s_recently_created(25)
    return render_template('guests/index.html',
                           guests=guests,
                           table='guests/_admin_table.html')

@app.route('/profile/', methods=['GET'])
@app.route('/guests/<guest_id>/', methods=['GET'])
def guests_show(guest_id=None):
    if guest_id:
        guest = Guest.read(int(guest_id))
    else:
        guest = g.uest

    if not guest:
        return render_404('Guest not found')
    else:
        return render_template('guests/show.html', guest=guest)
