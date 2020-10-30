#include <SoftwareSerial.h>
#include <WiFiEsp.h>
#include <PubSubClient.h>
#include <SimpleTimer.h>
#include <WifiUtil.h>
#include <DHT.h>
#include <MiniCom.h>

SoftwareSerial softSerial(2, 3);           // RX, TX

const char ssid[] = "Campus7_Room3_2.4";               // 네트워크 SSID
const char password[] = "12345678";       // 비밀번호
const char mqtt_server[] = "192.168.0.92"; // 라즈베리파이의 브로커 주소

MiniCom com;
DHT dht(7, DHT11); // DHT설정 - dht (디지털3, dht11)

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
        
        if (client.connect("livingroom_humitemp")) {
            Serial.println("connected");
            // subscriber로 등록
            client.subscribe("home/livingroom/#");  // 구독 신청
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void publish() {
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    char message[10];
    // 토픽 발행
    dtostrf(h, 5, 2, message);
    client.publish("home/livingroom/humi", message);
    dtostrf(t, 5, 2, message);
    client.publish("home/livingroom/temp", message);

    Serial.print(h);
    Serial.print(",");
    Serial.println(t);
}

// 2초 간격으로 publish
// SimpleTimer timer;

void setup() {
    com.init();
    wifi.init(ssid, password);
    mqtt_init();
    dht.begin();
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
