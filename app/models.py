from app import db

class Rooms(db.Model):
    """
    Create an Rooms table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'rooms'

    id = db.Column(db.String(60), primary_key=True)
    description = db.Column(db.String(200))
    

class Nodes(db.Model):
    """
    Create an Nodes table
    """
    __tablename__ = 'nodes'

    id = db.Column(db.String(60), primary_key=True)
    room = db.Column(db.String(60),  db.ForeignKey('rooms.id'))
    description = db.Column(db.String(200))
    connected = db.Column(db.String(20), nullable=True)
    

    def __repr__(self):
        return '<Nodes: {}>'.format(self.name)


class Sensors(db.Model):
    """
    Create an Sensors table
    """
    __tablename__ = 'sensors'

    id = db.Column(db.String(60), primary_key=True)
    node = db.Column(db.String(60),  db.ForeignKey('nodes.id'))
    description = db.Column(db.String(200))
    

    def __repr__(self):
        return '<Sensors: {}>'.format(self.name)



class Controllers(db.Model):
    """
    Create an Controllers table
    """
    __tablename__ = 'controllers'

    id = db.Column(db.String(60), primary_key=True)
    node = db.Column(db.String(60),  db.ForeignKey('nodes.id'))
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<Controllers: {}>'.format(self.name)



class Occupancy(db.Model):
    """
    Create an Occupancy table
    """
    __tablename__ = 'occupancy'

    id = db.Column(db.String(60), primary_key=True)
    node = db.Column(db.String(60),  db.ForeignKey('nodes.id'))
    timestamp = db.Column(db.DateTime)
    count = db.Column(db.Integer)

    def __repr__(self):
        return '<Occupancy: {}>'.format(self.name)




class Sensor_data(db.Model):
    """
    Create an Sensor_data table
    """
    __tablename__ = 'sensor_data'

    id = db.Column(db.String(60), primary_key=True)
    sensor = db.Column(db.String(60),  db.ForeignKey('sensors.id'))
    timestamp = db.Column(db.DateTime)
    data = db.Column(db.String(10))

    def __repr__(self):
        return '<Sensor_data: {}>'.format(self.name)


class Events(db.Model):
    """
    Create an Events table
    """
    __tablename__ = 'events'

    id = db.Column(db.String(60), primary_key=True)
    controller = db.Column(db.String(60),  db.ForeignKey('controllers.id'))
    timestamp = db.Column(db.DateTime)
    event = db.Column(db.String(10))

    def __repr__(self):
        return '<Events: {}>'.format(self.name)


