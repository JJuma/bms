# third-party imports
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mqtt import Mqtt

# local imports
from config import app_config

db = SQLAlchemy()
mqtt = Mqtt()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    #configure mqtt
    app.config['MQTT_BROKER_URL'] = '165.227.162.218'
    app.config['MQTT_BROKER_PORT'] = 1883 
    mqtt.init_app(app)
    
    Bootstrap(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
