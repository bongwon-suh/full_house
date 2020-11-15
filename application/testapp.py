import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
from gpiozero import  LED, Buzzer,PWMLED, Servo
from time import sleep
import RPi.GPIO as GPIO


# 거실조명
illu = PWMLED(17)
# 현관
entrance = Servo(23)
# 차고
garage = Servo(18)
# 창문
windo = Servo(22)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+ str(rc))
    if rc == 0:
        client.subscribe("home/#") # 연결 성공시 토픽 구독 신청
    else:
        print('연결 실패 : ', rc)
        
# 관련 토픽 메시지 수신 콜백 함수
def on_message(client, userdata, msg):
    value = float(msg.payload.decode())
    print(f" {msg.topic} {value}")

##################앱 관련 시작################
    if (msg.topic == "home/entrance"):
        if int(value)==1:
            entrance.max()
        else :
            entrance.min()
    elif (msg.topic == "home/garage"):
        if int(value)==1:
            garage.max()
        else :
            garage.min()
    elif (msg.topic == "home/livingroom/manual/windo"):
        windo.value = value
    elif (msg.topic == "home/livingroom/manual/illu"):
        illu.value = value
##################앱 관련 끝################
    
# 1. MQTT 클라이언트 객체 인스턴스화
client = mqtt.Client()

# 2. 관련 이벤트에 대한 콜백 함수 등록
client.on_connect = on_connect
client.on_message = on_message

try :
    # 3. 브로커 연결 / 브로커아이피 입력
    client.connect("192.168.25.3")
    
    # 4. 메시지 루프 - 이벤트 발생시 해당 콜백 함수 호출됨
    client.loop_forever()

    client.loop_start()
    # 새로운 스래드를 가동해서 운영 - daemon 스레드  Thread.setDaemon(True)
except Exception as err:
	print('에러 : %s'%err)
    
print("--- End Main Thread ---")
