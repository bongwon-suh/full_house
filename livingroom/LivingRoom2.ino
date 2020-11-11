#include <SoftwareSerial.h>
#include <WiFiEsp.h>
#include <PubSubClient.h>
#include <SimpleTimer.h>
#include <WifiUtil.h>
#include <MiniCom.h>
#include <AnalogSensor.h>
#include <Flame.h>
#include <VibrateDetector.h>

SoftwareSerial softSerial(2, 3);           // RX, TX

const char ssid[] = "Campus7_Room3_2.4";               // 네트워크 SSID
const char password[] = "12345678";       // 비밀번호
const char mqtt_server[] = "192.168.0.92"; // 라즈베리파이의 브로커 주소

MiniCom com;

AnalogSensor gasdetector(A0,0,255);
Flame flame(9);
VibrateDetector vibrate(5,A1); //din, Aout

// MQTT용 WiFi 클라이언트 객체 초기화
WifiUtil wifi(2, 3);
WiFiEspClient espClient;
PubSubClient client(espClient);

void mqtt_init() {
    client.setServer(mqtt_server, 1883);
}
// MQTT 서버에 접속될 때까지 재접속 시도
void reconnect() {

    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        
        if (client.connect("livingroom_2")) {
            Serial.println("connected");
            // subscriber로 등록
            client.subscribe("home/livingroom/#");  // 구독 신청
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 1 seconds");
            delay(1000);
        }
    }
}

void publish() {
    float gas = gasdetector.read();
    float flame_ = flame.read();
    float vibe = vibrate.read();

    char message[10];
    
    // 토픽 발행

    dtostrf(gas, 5, 2, message);
    client.publish("home/livingroom/gasdetector", message);

    if (flame_ != 0) {
      dtostrf(flame_, 5, 2, message);
      client.publish("home/livingroom/flame",message);
      }

    dtostrf(vibe, 5, 2, message);
    client.publish("home/livingroom/vibrator", message);


    Serial.print(gas);
    Serial.print(",");
    Serial.print(flame_);
    Serial.print(",");
    Serial.println(vibe);

}

void setup() {
    com.init();
    wifi.init(ssid, password);
    mqtt_init();
    pinMode(13, OUTPUT);
    digitalWrite(13, LOW);
    com.setInterval(5000,publish);

}

void loop() {
    if (!client.connected()) {  // MQTT가 연결 X
        reconnect();
    }

    client.loop();
    com.run();
}
