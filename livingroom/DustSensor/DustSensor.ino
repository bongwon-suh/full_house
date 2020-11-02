#include <SoftwareSerial.h>
#include <WiFiEsp.h>
#include <PubSubClient.h>
#include <SimpleTimer.h>
#include <WifiUtil.h>
#include <MiniCom.h>
#include "DustSensor.h"

DustSensor dust(8);

SoftwareSerial softSerial(2, 3);           // RX, TX

const char ssid[] = "Campus7_Room3_2.4";               // 네트워크 SSID
const char password[] = "12345678";       // 비밀번호
const char mqtt_server[] = "192.168.0.92"; // 라즈베리파이의 브로커 주소

MiniCom com;

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
        
        if (client.connect("livingroom_dustsensor")) {
            Serial.println("connected");
            // subscriber로 등록
            client.subscribe("home/home1/#");  // 구독 신청
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void publish() {
    int dust_value = dust.getDust();
    char message[10];
    // 토픽 발행
    dtostrf(dust_value, 5, 2, message);
    client.publish("iot/home/dust", message);
    Serial.println(dust_value);
}

// 2초 간격으로 publish
// SimpleTimer timer;

void setup() {
    com.init();
    wifi.init(ssid, password);
    mqtt_init();
    pinMode(13, OUTPUT);
    digitalWrite(13, LOW);
    com.setInterval(2000,publish);

}

void loop() {
    if (!client.connected()) {  // MQTT가 연결 X
        reconnect();
    }
    client.loop();
    com.run();
}
