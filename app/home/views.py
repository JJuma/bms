from flask import abort, render_template

from . import home

#################################
from ..models import Rooms

@home.route('/admin/dashboard')
def admin_dashboard():
    
    rooms = Rooms.query.all()

    return render_template('home/admin_dashboard.html',rooms=rooms, title="Dashboard")
#################################


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


# @home.route('/admin/dashboard')
# def admin_dashboard():
#     return render_template('home/admin_dashboard.html', title="Dashboard")




