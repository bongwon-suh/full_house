import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


####flame alarm system####
#부저 세팅
buzzerpin = 18
GPIO.setup(buzzerpin, GPIO.OUT)
GPIO.setmode(GPIO.BCM)
# GPIO 18번 핀을 출력으로 설정
GPIO.setup(buzzerpin, GPIO.OUT)
# PWM 인스턴스 p를 만들고 GPIO 18번을 PWM 핀으로 설정, 주파수 = 100Hz
flmbuzzer = GPIO.PWM(buzzerpin, 100)

#LED 세팅
led_pin = 17
GPIO.setup(led_pin, GPIO.OUT)

#서보모터 세팅
servo_pin = 16
GPIO.setup(servo_pin, GPIO.OUT)
flmservo = GPIO.PWM(servo_pin, 50)

def alarmPiezo():
    flmbuzzer.start() # PWM 시작 , 듀티사이클 10 (충분)
    return 0

def lockValveLed():
    GPIO.output(led_pin,0)
    return 0

def lockValveServo():
    flmservo.ChangeDutyCycle(180)
    return 0

# LED 핀을 가스 잠금장치로 표현

# 브로커 접속 시도 결과 처리 콜백 함수
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+ str(rc))
    if rc == 0:
        client.subscribe("iot/#") # 연결 성공시 토픽 구독 신청
    else:
        print('연결 실패 : ', rc)


# 관련 토픽 메시지 수신 콜백 함수
def on_message(client, userdata, msg):
    value = float(msg.payload.decode())
    print(f" {msg.topic} {value}")
    print(type(msg.topic))
    # print(float(msg.payload.decode())


    #msg 토픽 주소가 iot/home/livingroom/flame일 경우
    if msg.topic == "iot/home/livingroom/flame":
        value = float(msg.payload.decode())
        # value값을 읽고 state 가 0이라면
        if value == 0.0:
            flmbuzzer.stop()
            flmservo.ChangeDutyCycle(2.5)
            GPIO.output(led_pin,1)
        else :
            # 0이 아니면,
            # 피에조 부저 알람
            alarmPiezo()
            # 그리고 가스밸브 잠금
            lockValveLed()
            lockValveServo()


# 1. MQTT 클라이언트 객체 인스턴스화
client = mqtt.Client()
# 2. 관련 이벤트에 대한 콜백 함수 등록
client.on_connect = on_connect
client.on_message = on_message

try :
    # 3. 브로커 연결
    client.connect("localhost")
    # 4. 메시지 루프 - 이벤트 발생시 해당 콜백 함수 호출됨
    client.loop_forever()
except Exception as err:
    print('에러 : %s'%err)