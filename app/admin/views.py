from flask import abort, flash, redirect, render_template, url_for

from . import admin
from .forms import RoomsForm, NodesForm, ControllersForm, SensorsForm
from .. import db
from ..models import Rooms, Nodes, Sensors, Controllers


# Rooms Views

@admin.route('/rooms', methods=['GET', 'POST'])
def list_rooms():
    """
    List all rooms
    """
    rooms = Rooms.query.all()

    return render_template('admin/rooms/rooms.html',
                           rooms=rooms, title="Rooms")


@admin.route('/rooms/add', methods=['GET', 'POST'])
def add_room():
    """
    Add a room to the database
    """

    add_room = True

    form = RoomsForm()
    if form.validate_on_submit():
        room = Rooms(id=form.id.data,
                                description=form.description.data)
        try:
            # add room to the database
            db.session.add(room)
            db.session.commit()
            flash('You have successfully added a new room.')
        except:
            # in case room name already exists
            flash('Error: room name already exists.')

        # redirect to rooms page
        return redirect(url_for('admin.list_rooms'))

    # load room template
    return render_template('admin/rooms/room.html', action="Add",
                           add_room=add_room, form=form,
                           title="Add Room")


@admin.route('/rooms/edit/<string:id>', methods=['GET', 'POST'])
def edit_room(id):
    """
    Edit a room
    """

    add_room = False

    room = Rooms.query.get_or_404(id)
    form = RoomsForm(obj=room)
    if form.validate_on_submit():
        room.id = form.id.data
        room.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the room.')

        # redirect to the rooms page
        return redirect(url_for('admin.list_rooms'))

    form.description.data = room.description
    form.id.data = room.id
    return render_template('admin/rooms/room.html', action="Edit",
                           add_room=add_room, form=form,
                           room=room, title="Edit Rooms")


@admin.route('/rooms/delete/<string:id>', methods=['GET', 'POST'])
def delete_room(id):
    """
    Delete a room from the database
    """

    room = Rooms.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    flash('You have successfully deleted the room.')

    # redirect to the rooms page
    return redirect(url_for('admin.list_rooms'))

    return render_template(title="Delete Rooms")





#Nodes Views

@admin.route('/nodes', methods=['GET', 'POST'])
def list_nodes():
    """
    List all nodes
    """

    nodes = Nodes.query.all()

    return render_template('admin/nodes/nodes.html',
                           nodes=nodes, title="Nodes")

@admin.route('/nodes/add', methods=['GET', 'POST'])
def add_node():
    """
    Add a node to the database
    """

    add_node = True

    form = NodesForm()
    if form.validate_on_submit():
        node = Nodes(id=form.id.data,
                        room=form.room.data,
                                 description=form.description.data)
        try:
            # add node to the database
            db.session.add(node)
            db.session.commit()
            flash('You have successfully added a new node.')
        except:
            # in case node name already exists
            flash('Error: node name already exists.')

        # redirect to nodes page
        return redirect(url_for('admin.list_nodes'))

    # load node template
    return render_template('admin/nodes/node.html', action="Add",
                           add_node=add_node, form=form,
                           title="Add Node")

@admin.route('/nodes/edit/<string:id>', methods=['GET', 'POST'])
def edit_node(id):
    """
    Edit a node
    """

    add_node = False

    node = Nodes.query.get_or_404(id)
    form = NodesForm(obj=node)
    if form.validate_on_submit():
        node.id = form.id.data
        node.room = form.room.data
        node.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the node.')

        # redirect to the nodes page
        return redirect(url_for('admin.list_nodes'))

    form.id.data = node.id
    form.room.data = node.room
    
    return render_template('admin/nodes/node.html', action="Edit",
                           add_node=add_node, form=form,
                           node=node, title="Edit Nodes")

@admin.route('/nodes/delete/<string:id>', methods=['GET', 'POST'])
def delete_node(id):
    """
    Delete a node from the database
    """

    node = Nodes.query.get_or_404(id)
    db.session.delete(node)
    db.session.commit()
    flash('You have successfully deleted the node.')

    # redirect to the nodes page
    return redirect(url_for('admin.list_nodes'))

    return render_template(title="Delete Nodes")



#Sensor Views

@admin.route('/sensors', methods=['GET', 'POST'])
def list_sensors():
    """
    List all sensors
    """

    sensors = Sensors.query.all()

    return render_template('admin/sensors/sensors.html',
                           sensors=sensors, title="Sensors")

@admin.route('/sensors/add', methods=['GET', 'POST'])
def add_sensor():
    """
    Add a sensor to the database
    """

    add_sensor = True

    form = SensorsForm()
    if form.validate_on_submit():
        sensor = Sensors(id=form.id.data,
                            node=form.node.data,
                                description=form.description.data)
        try:
            # add sensor to the database
            db.session.add(sensor)
            db.session.commit()
            flash('You have successfully added a new sensor.')
        except:
            # in case sensor name already exists
            flash('Error: sensor name already exists.')

        # redirect to sensors page
        return redirect(url_for('admin.list_sensors'))

    # load sensor template
    return render_template('admin/sensors/sensor.html', action="Add",
                           add_sensor=add_sensor, form=form,
                           title="Add Sensor")

@admin.route('/sensors/edit/<string:id>', methods=['GET', 'POST'])
def edit_sensor(id):
    """
    Edit a sensor
    """

    add_sensor = False

    sensor = Sensors.query.get_or_404(id)
    form = SensorsForm(obj=sensor)
    if form.validate_on_submit():
        sensor.id = form.id.data
        sensor.node = form.node.data
        sensor.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the sensor.')

        # redirect to the sensors page
        return redirect(url_for('admin.list_sensors'))

    form.id.data = sensor.id
    form.node.data = sensor.node
    form.description.data = sensor.description
    return render_template('admin/sensors/sensor.html', action="Edit",
                           add_sensor=add_sensor, form=form,
                           sensor=sensor, title="Edit Sensors")

@admin.route('/sensors/delete/<string:id>', methods=['GET', 'POST'])
def delete_sensor(id):
    """
    Delete a sensor from the database
    """

    sensor = Sensors.query.get_or_404(id)
    db.session.delete(sensor)
    db.session.commit()
    flash('You have successfully deleted the sensor.')

    # redirect to the sensors page
    return redirect(url_for('admin.list_sensors'))

    return render_template(title="Delete Sensors")








#Controller Views

@admin.route('/controllers', methods=['GET', 'POST'])
def list_controllers():
    """
    List all controllers
    """

    controllers = Controllers.query.all()

    return render_template('admin/controllers/controllers.html',
                           controllers=controllers, title="Controllers")

@admin.route('/controllers/add', methods=['GET', 'POST'])
def add_controller():
    """
    Add a controller to the database
    """

    add_controller = True

    form = ControllersForm()
    if form.validate_on_submit():
        controller = Controllers(id=form.id.data,
                                    node=form.node.data,
                                        description=form.description.data)
        try:
            # add controller to the database
            db.session.add(controller)
            db.session.commit()
            flash('You have successfully added a new controller.')
        except:
            # in case controller name already exists
            flash('Error: controller name already exists.')

        # redirect to controllers page
        return redirect(url_for('admin.list_controllers'))

    # load controller template
    return render_template('admin/controllers/controller.html', action="Add",
                           add_controller=add_controller, form=form,
                           title="Add Controller")

@admin.route('/controllers/edit/<string:id>', methods=['GET', 'POST'])
def edit_controller(id):
    """
    Edit a controller
    """

    add_controller = False

    controller = Controllers.query.get_or_404(id)
    form = ControllersForm(obj=controller)
    if form.validate_on_submit():
        controller.id = form.id.data
        controller.node = form.node.data
        controller.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the controller.')

        # redirect to the controllers page
        return redirect(url_for('admin.list_controllers'))

    form.id.data = controller.id
    form.node.data = controller.node
    form.description.data = controller.description
    return render_template('admin/controllers/controller.html', action="Edit",
                           add_controller=add_controller, form=form,
                           controller=controller, title="Edit Controllers")

@admin.route('/controllers/delete/<string:id>', methods=['GET', 'POST'])
def delete_controller(id):
    """
    Delete a controller from the database
    """

    controller = Controllers.query.get_or_404(id)
    db.session.delete(controller)
    db.session.commit()
    flash('You have successfully deleted the controller.')

    # redirect to the controllers page
    return redirect(url_for('admin.list_controllers'))

    return render_template(title="Delete Controllers")





