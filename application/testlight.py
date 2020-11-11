import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
from gpiozero import  LED, Buzzer,PWMLED
from time import sleep
import RPi.GPIO as GPIO


led = PWMLED(17)
state = 0
manuillu = 0
manutemp = 0


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
    illu = 0
    global state
    global manualtemp
    if (msg.topic == "home/livingroom/manualstate"):
        state = value
    elif (msg.topic == "home/livingroom/manual/illu"):
        manuillu = value
        if int(state) == 1 :
            led.value = (manuillu/10)

    elif (msg.topic == "home/livingroom/manual/temp"):
        manutemp = value


    elif msg.topic == "home/livingroom/temp":
        t = value
        if int(state) == 1:    
            if t > manualtemp+1:
                hitter.off()
                aircon.on()
            elif t < manualtemp-1:
                hitter.on()
                aircon.off()
            else:
                hitter.off()
                aircon.off()
    
    elif msg.topic == "home/livingroom/humi":
        h = value
        if int(state) == 1:
            if h > manualhumi+1:
                fan.on()
            else :
                fan.off()
    
# 1. MQTT 클라이언트 객체 인스턴스화
client = mqtt.Client()

# 2. 관련 이벤트에 대한 콜백 함수 등록
client.on_connect = on_connect
client.on_message = on_message

try :
    # 3. 브로커 연결 / 브로커아이피 입력
    client.connect("0.0.0.0")
    
    # 4. 메시지 루프 - 이벤트 발생시 해당 콜백 함수 호출됨
    client.loop_forever()

    client.loop_start()
    # 새로운 스래드를 가동해서 운영 - daemon 스레드  Thread.setDaemon(True)
except Exception as err:
	print('에러 : %s'%err)
    
print("--- End Main Thread ---")
