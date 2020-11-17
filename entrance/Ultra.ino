#include <WiFiEsp.h>
#include <SoftwareSerial.h>
#include <PubSubClient.h>
#include <Arduino.h>
#include <WifiUtil.h>
#include <MiniCom.h>
#include <Ultra.h>

SoftwareSerial SoftwareSerial(2, 3);

const char ssid[] = "Campus7_Room3_2.4";               // 네트워크 SSID
const char password[] = "12345678";       // 비밀번호
const char mqtt_server[] = "192.168.0.92";

WifiUtil wifi(2, 3);
WiFiEspClient espClient;
PubSubClient client(espClient);

Ultra ultra(7, 8);
MiniCom com;

void mqtt_init() {
    client.setServer(mqtt_server, 1883);
}

void reconnect() {
    while(!client.connected()) {
        Serial.print("Attempting MQTT connection....");

        if(client.connect("UltraEspClient")) {
            Serial.println("connected");
            client.subscribe("home/entrance/ultra");
        }
        else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println("try again in 5 seconds");
            delay(5000);
        }
    }
}

void publish() {
    int i = ultra.read();
    char message[10];

    dtostrf(i, 5, 2, message);
    client.publish("home/entrance/ultra", message);

    Serial.println(i);
}

void setup()
{
	Serial.begin(9600);
    wifi.init(ssid, password);
    mqtt_init();
    com.setInterval(5000, publish);
}

void loop()
{
    if (!client.connected()) {
        reconnect();
    }

    client.loop();
    com.run();

}
