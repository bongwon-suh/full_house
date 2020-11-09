from flask import Flask, request, make_response, jsonify
from flask import render_template
import json
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from random import sample
from bson.json_util import loads, dumps
from bson import json_util
from time import time
from gpiozero import  LED

client = mqtt.Client()
client.connect("192.168.0.7", 1883) #MQTT 서버에 연결
client.loop(2)

mongodb = MongoClient("mongodb://192.168.0.2:27017/")
db = mongodb.full_house
collection = db.sensors
led = LED(26)

app = Flask(__name__)
# GPIO.setmode(GPIO.BOARD) #BOARD는 커넥터 pin번호 사용
# GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

@app.route("/")
def index():
    query = {"topic":"iot/home1/temp"}
    labels = collection.find(query).sort("reg_date").limit(10)
    values = dumps(list(collection.find(query).sort("reg_date").limit(10)))
    # json_list = json.dumps(list(labels))
    # results = dumps(list(result))
    # print(labels)
    print(values)
    # print(type(json_list))
    query2 = {"topic":"home/livingroom/led"}
    label = db.states.find_one(query2)
    
    return render_template("index.html", labels=labels, values=values, label=label)
    

@app.route("/led_on")
def led_on():
    try:
        client.publish("home/livingroom/led", "1")
        # led.on()
        return (''), 204
    except expression as identifier:
        return (''), 204

@app.route("/led_off")
def led_off():
    try:
        client.publish("home/livingroom/led", "0")
        # led.off()
        return (''), 204
    except expression as identifier:
        return (''), 204

@app.route("/live-data")
def live_data():
    query = {"topic":"home/livingroom/humi"}
    labels = collection.find(query).sort("reg_date", -1).limit(1)
    for i in labels:      
        labels_dict = {'reg_date':i['reg_date'].strftime('%H:%M:%S'), 'value':i['value']}
        # labels_list = [i['reg_date'].strftime('%H:%M:%S'), i['value']]
        labels_list = [time()*1000+3, i['value']]
    response = make_response(json.dumps(labels_list))
    print(type(response))
    response.content_type = 'application/json'
    return response

@app.route("/live-data2")
def live_data2():
    query = {"topic":"home/livingroom/temp"}
    labels = collection.find(query).sort("reg_date", -1).limit(1)
    for i in labels:      
        labels_dict = {'reg_date':i['reg_date'].strftime('%H:%M:%S'), 'value':i['value']}
        # labels_list = [i['reg_date'].strftime('%H:%M:%S'), i['value']]
        labels_list = [time()*1000+3, i['value']]
    response = make_response(json.dumps(labels_list))
    print(type(response))
    response.content_type = 'application/json'
    return response

@app.route("/live-data3")
def live_data3():
    query = {"topic":"home/livingroom/dust"}
    labels = collection.find(query).sort("reg_date", -1).limit(1)
    for i in labels:      
        labels_dict = {'reg_date':i['reg_date'].strftime('%H:%M:%S'), 'value':i['value']}
        # labels_list = [i['reg_date'].strftime('%H:%M:%S'), i['value']]
        labels_list = [time()*1000+3, i['value']]
    response = make_response(json.dumps(labels_list))
    print(type(response))
    response.content_type = 'application/json'
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0")