from flask import abort, flash, redirect, render_template, url_for
from collections import defaultdict
import json
import time

from . import admin
from .. import db, mqtt
from ..models import Rooms, Nodes, Sensors, Controllers


#sys error for windows
import os
import sys
if sys.platform.lower() == "win32": 
    os.system('color')


#database fetch data for display on website
@admin.route('/sql/<room>')
@admin.route('/sql/<room>/<update>')
def scheduled_sql(room,update = None):
    """
        process chart data
    """
    
    sensors = ["Temperature1","Humidity1","Energy1","Occupancy1"]
    length = len(sensors)
    for i in range(length):
        sensors[i] = room + sensors[i]

    data = defaultdict(list) 

    #on update
    if update:
        for sensor in sensors:
            sql = ( f""" SELECT timestamp, data FROM
                    (SELECT sensors.node, sensor_data.sensor, sensor_data.timestamp, sensor_data.data 
                        FROM sensors,sensor_data WHERE sensors.id = '{sensor}' and sensor_data.sensor = '{sensor}'
                        ORDER BY timestamp DESC LIMIT 10)sub,
                    nodes
                    WHERE nodes.id = node and nodes.room = '{room}' 
                    ORDER BY timestamp DESC LIMIT 1;
                    """)
            result = db.session.execute(sql)

            for x in result:
                x = list(x)
                data[sensor+"_time"] = ( x[0].strftime("%Y-%m-%d %H:%M:%S") )
                data[sensor+"_data"] = ( x[1] )

        data = json.dumps(data)
        #print(data)

    #on 1st reload
    else:
        for sensor in sensors:
            sql = ( f""" SELECT timestamp, data FROM 
                    (SELECT sensors.node, sensor_data.sensor, sensor_data.timestamp, sensor_data.data FROM 
                        sensors,sensor_data WHERE sensors.id = '{sensor}' and sensor_data.sensor = '{sensor}'
                        ORDER BY timestamp DESC LIMIT 30)sub,
                    nodes
                    WHERE nodes.id = node and nodes.room = '{room}' 
                    ORDER BY timestamp DESC LIMIT 10;
                    """)
            result = db.session.execute(sql)
            
            for x in result:
                x = list(x)
                data[sensor+"_time"].append( x[0].strftime("%Y-%m-%d %H:%M:%S") )
                data[sensor+"_data"].append( x[1] )

        data = json.dumps(data)
        #print(data)
        
    return data


@admin.route('/mqtt/<room>/<controller>/<event>')
def mqtt_func(room,controller,event):
    message = {controller:int(event)}
    message = json.dumps(message)
    mqtt.publish("bms/"+room+"/controller/1",message)
    return message