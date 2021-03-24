from flask import abort, flash, redirect, render_template, url_for
from collections import defaultdict
import json

from . import admin
from .. import db
from ..models import Rooms, Nodes, Sensors, Controllers

#mqtt import
import paho.mqtt.client as mqtt
import time

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
    
    sensors = ["Temperature1","Humidity1","airQuality1","Energy1","Occupancy1"]
    length = len(sensors)
    for i in range(length):
        sensors[i] = room + sensors[i]

    data = defaultdict(list) 

    #on update
    if update:
        for sensor in sensors:
            sql = ( f""" SELECT timestamp, data FROM
                    (SELECT sensors.node, sensor_data.sensor, sensor_data.timestamp, sensor_data.data 
                        FROM sensors,sensor_data WHERE sensors.id = sensor_data.sensor ORDER BY timestamp DESC LIMIT 10)sub,
                    nodes
                    WHERE nodes.id = node and nodes.room = '{room}' and sensor = '{sensor}'
                    ORDER BY timestamp DESC LIMIT 1;
                    """)
            result = db.session.execute(sql)

            for x in result:
                x = list(x)
                data[sensor+"_time"] = ( x[0].strftime("%Y-%m-%d %H:%M:%S") )
                data[sensor+"_data"] = ( x[1] )

        data = json.dumps(data)
        # print(data)

    #on 1st reload
    else:
        for sensor in sensors:
            sql = ( f""" SELECT timestamp, data FROM 
                    (SELECT sensors.node, sensor_data.sensor, sensor_data.timestamp, sensor_data.data FROM 
                        sensors,sensor_data WHERE sensors.id = sensor_data.sensor ORDER BY timestamp DESC LIMIT 30)sub,
                    nodes
                    WHERE nodes.id = node and nodes.room = '{room}' and sensor = '{sensor}'
                    ORDER BY timestamp DESC LIMIT 10;
                    """)
            result = db.session.execute(sql)
            
            for x in result:
                x = list(x)
                data[sensor+"_time"].append( x[0].strftime("%Y-%m-%d %H:%M:%S") )
                data[sensor+"_data"].append( x[1] )

        data = json.dumps(data)
        # print(data)
        
    return data




# MQTT configuration for buttons

def on_log(client, userdata, level, buf):
    print("log: "+buf)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        print("connected ok")
    else:
        client.bad_connection_flag = True
        print("bad connection return code=",rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("disconnecting reason: "+ str(rc))
    client.connected_flag = False
    client.disconnect_flag = True

def on_message(client, userdata, msg):
    #topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8"))
    print("message recieved ", m_decode)




@admin.route('/mqtt/<room>/<controller>/<event>')
def mqtt_func(room,controller,event):
    broker = "165.227.162.218"
    #create new instance
    client = mqtt.Client("web")

    #bind call back function
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    # client.on_log = on_log
    client.on_message = on_message

    print ("connecting to broker " + broker )

    #create flag in class
    mqtt.Client.connected_flag = False 
    mqtt.Client.bad_connection_flag = False
    mqtt.Client.disconnect_flag = False

    #connect to broker
    try:
        client.connect(broker, port=1883, keepalive=60, bind_address="")
    except:
        print("connection failed")
        exit(1)

    #start loop
    client.loop_start()
    # time.sleep(4)# Wait for connection setup to complete

    #wait in loop for connection to be established
    while not client.connected_flag and not client.bad_connection_flag:
        print("In wait loop")
        time.sleep(1)
    if client.bad_connection_flag:
        client.loop_stop()
        # sys.exit()

    print("In main loop")
    
    # bms/room1/controller/1
    # client.subscribe("bms/"+room+"/controller/1")
    message = {controller:event}
    message = json.dumps(message)
    client.publish("bms/"+room+"/controller/1",message)

    #stop loop
    client.loop_stop()
    #disconnect
    client.disconnect()

    return message