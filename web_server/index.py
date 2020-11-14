from flask import Flask, request, make_response, jsonify
from flask import render_template
import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from random import sample
from bson.json_util import loads, dumps
from time import time

client = mqtt.Client()
client.connect("192.168.0.92", 1883) #MQTT 서버에 연결
client.loop_start()

mongodb = MongoClient("mongodb://192.168.0.84:27017/")
db = mongodb.full_house
collection = db.sensors

app = Flask(__name__)
# GPIO.setmode(GPIO.BOARD) #BOARD는 커넥터 pin번호 사용
# GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

@app.route("/")
def index():
    query_light = {"topic":"home/livingroom_state/led"}
    light = db.states.find_one(query_light)
    
    query_aircon = {"topic":"home/livingroom_state/aircon"}
    aircon = db.states.find_one(query_aircon)

    query_heater = {"topic":"home/livingroom_state/heater"}
    heater = db.states.find_one(query_heater)

    query_airdry = {"topic":"home/livingroom_state/airdry"}
    airdry = db.states.find_one(query_airdry)

    query_blind = {"topic":"home/livingroom_state/blind"}
    blind = db.states.find_one(query_blind)

    query_fan = {"topic":"home/livingroom_state/fan"}
    fan = db.states.find_one(query_fan)

    query_gas = {"topic":"home/livingroom_state/gas"}
    gas = db.states.find_one(query_gas)

    query_auto = {"topic":"home/livingroom_state/auto"}
    auto = db.states.find_one(query_auto)

    query_flame = {"topic":"home/livingroom/flame"}
    flame = db.sensors.find(query_flame)

    return render_template("index.html", light=light, aircon=aircon, heater=heater, airdry=airdry,
                                         blind=blind, fan=fan, gas=gas, auto=auto, flame=flame)
    
@app.route("/led_on")
def led_on():
    try:
        client.publish("home/livingroom_state/led", "1")
        return "ok"
    except expression as identifier:
        return "fail"

@app.route("/led_off")
def led_off():
    try:
        client.publish("home/livingroom_state/led", "0")
        return "ok"
    except expression as identifier:
        return "fail"


@app.route("/aircon_on")
def aircon_on():
    try:
        client.publish("home/livingroom_state/aircon", "1")
        return "ok"
    except expression as identifier:
        return "fail"

@app.route("/aircon_off")
def aircon_off():
    try:
        client.publish("home/livingroom_state/aircon", "0")
        return "ok"
    except expression as identifier:
        return "fail"


@app.route("/heater_on")
def heater_on():
    try:
        client.publish("home/livingroom_state/heater", "1")
        return "ok"
    except expression as identifier:
        return "fail"

@app.route("/heater_off")
def heater_off():
    try:
        client.publish("home/livingroom_state/heater", "0")
        return "ok"
    except expression as identifier:
        return "fail"


@app.route("/airdry_on")
def airdry_on():
    try:
        client.publish("home/livingroom_state/airdry", "1")
        return "ok"
    except expression as identifier:
        return "fail"

@app.route("/airdry_off")
def airdry_off():
    try:
        client.publish("home/livingroom_state/airdry", "0")
        return "ok"
    except expression as identifier:
        return "fail"

@app.route("/blind_on")
def blind_on():
    try:
        client.publish("home/livingroom_state/blind", "1")
        return "ok"
    except expression as identifier:
        return "fail"

@app.route("/blind_off")
def blind_off():
    try:
        client.publish("home/livingroom_state/blind", "0")
        return "ok"
    except expression as identifier:
        return "fail"

@app.route("/fan_on")
def fan_on():
    try:
        client.publish("home/livingroom_state/fan", "1")
        return "ok"
    except expression as identifier:
        return "fail"

@app.route("/fan_off")
def fan_off():
    try:
        client.publish("home/livingroom_state/fan", "0")
        return "ok"
    except expression as identifier:
        return "fail"



@app.route("/gas_on")
def gas_on():
    try:
        client.publish("home/livingroom_state/gas", "1")
        return "ok"
    except expression as identifier:
        return "fail"

@app.route("/gas_off")
def gas_off():
    try:
        client.publish("home/livingroom_state/gas", "0")
        return "ok"
    except expression as identifier:
        return "fail"


@app.route("/auto_on")
def auto_on():
    try:
        client.publish("home/livingroom_state/auto", "1")
        return "ok"
    except expression as identifier:
        return "fail"

@app.route("/auto_off")
def auto_off():
    try:
        client.publish("home/livingroom_state/auto", "0")
        return "ok"
    except expression as identifier:
        return "fail"

# 습도 차트
@app.route("/live-data")
def live_data():
    query = {"topic":"home/livingroom/humi"}
    labels = collection.find(query).sort("reg_date", -1).limit(1)
    for i in labels:      
        labels_dict = {'reg_date':i['reg_date'].strftime('%H:%M:%S'), 'value':i['value']}
        # labels_list = [i['reg_date'].strftime('%H:%M:%S'), i['value']]
        labels_list = [time()*1000, i['value']]
    response = make_response(json.dumps(labels_list))
    print(type(response))
    response.content_type = 'application/json'
    return response

# 온도 차트
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


# 미세먼지 차트
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

# 미세먼지 차트
@app.route("/live-data4")
def live_data4():
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

# 미세먼지 차트
@app.route("/live-data5")
def live_data5():
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


# 미세먼지 차트
@app.route("/live-data6")
def live_data6():
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