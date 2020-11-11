import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
from gpiozero import  LED
from time import sleep

# DB연결
mongodb = MongoClient("mongodb://192.168.0.84:27017/")
db = mongodb.full_house
red = LED(17)
# 브로커 접속 시도 결과 처리 콜백 함수
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+ str(rc))
    if rc == 0:
        client.subscribe("home/#") # 연결 성공시 토픽 구독 신청
    else:
        print('연결 실패 : ', rc)
        
# 관련 토픽 메시지 수신 콜백 함수
def on_message(client, userdata, msg):
    value = float(msg.payload.decode())
    # nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
    print(f" {msg.topic} {value}")
    # MongoDB에 데이터 저장하는 코드가 여기에서 이루어짐

    if '_state' in msg.topic:
        db.states.update_one(
            {'topic':msg.topic},
            {'$set':
                {"state":value}
            }
        )
    else:      
        doc = {
            "topic" : msg.topic,
            "value" : value,
            "reg_date" : datetime.now()
        }
        db.sensors.insert_one(doc)

    
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
