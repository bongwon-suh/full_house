import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
from gpiozero import  LED, Buzzer
from time import sleep
import RPi.GPIO as GPIO

# 가스감지기 피에조부저
w_signal = Buzzer(13)

# 조도센서 셋팅
led = LED(16)
SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
blind = GPIO.PWM(SERVO_PIN, 50)
blind.start(0)

# 온습도 센서 셋팅
hitter = LED(27)
aircon = LED(17)
airdry = LED(22)

#미세먼지 센서 셋팅
fan = LED(19)

#불꽃감지 센서 셋팅(밸브ver)
SERVO_v_PIN = 23
GPIO.setup(SERVO_v_PIN, GPIO.OUT)
valve = GPIO.PWM(SERVO_v_PIN, 50)
valve.start(0)
#불꽃감지 센서 셋팅
# valve = LED(23)

# DB연결
mongodb = MongoClient("mongodb://192.168.0.84:27017/")
db = mongodb.full_house
# 브로커 접속 시도 결과 처리 콜백 함수
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+ str(rc))
    if rc == 0:
        client.subscribe("home/livingroom/#") # 연결 성공시 토픽 구독 신청
    else:
        print('연결 실패 : ', rc)
        
# 관련 토픽 메시지 수신 콜백 함수
def on_message(client, userdata, msg):
    value = float(msg.payload.decode())
    print(f" {msg.topic} {value}")
    
    # 가스감지기 컨트롤
    if msg.topic == "home/livingroom/gasdetector":
        if value > 160:
            print("Warnning!!")
            w_signal.beep(0.5,0.5)
        else:
            w_signal.off()
    
    # 조도센서 컨트롤
    elif msg.topic == "home/livingroom/illu":
        if value < 15: # 어두울 때
            led.on()
            blind.ChangeDutyCycle(7.5) # 90도
        elif value >= 30: # 밝을 때
            led.off()
            blind.ChangeDutyCycle(12.5) # 180도
    
    # 습도센서 컨트롤
    elif msg.topic == "home/livingroom/humi":
        h = value
        if h > 38:
            airdry.on()
        else:
             airdry.off()

    # 온도센서 컨트롤         
    elif msg.topic == "home/livingroom/temp":
        t = value
        if t > 27:
            hitter.off()
            aircon.on()
        elif t < 22:
            hitter.on()
            aircon.off()
        else:
            hitter.off()
            aircon.off()
    
    elif msg.topic == "home/livingroom/dust":
        if value > 100:
            fan.on()
        else:
             fan.off()  

    # 불꽃센서 컨트롤(servo.)
    elif msg.topic == "home/livingroom/flame":
        if value != 0 :
            valve.ChangeDutyCycle(12.5) #잠금
        else:
            valve.ChangeDutyCycle(2.5) #열림
    # 불꽃센서 컨트롤(led.)
    # elif msg.topic == "home/livingroom/flame":
    #     if value == 0 :
    #         valve.on()
    #     else:
    #         valve.off()

    
# 1. MQTT 클라이언트 객체 인스턴스화
client = mqtt.Client()

# 2. 관련 이벤트에 대한 콜백 함수 등록
client.on_connect = on_connect
client.on_message = on_message

try :
    # 3. 브로커 연결 / 브로커아이피 입력
    client.connect("192.168.0.92")
    
    # 4. 메시지 루프 - 이벤트 발생시 해당 콜백 함수 호출됨
    client.loop_forever()

    # client.loop_start()
    # 새로운 스래드를 가동해서 운영 - daemon 스레드  Thread.setDaemon(True)
except Exception as err:
	print('에러 : %s'%err)
    
print("--- End Main Thread ---")
