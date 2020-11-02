#include <WiFiEsp.h>
#include <SoftwareSerial.h>
#include <PubSubClient.h>
#include <Arduino.h>
#include <Servo.h>
#include <AnalogSensor.h>
#include <Led.h>
#include <WifiUtil.h>
#include <MiniCom.h>

SoftwareSerial SoftwareSerial(2, 3);

const char ssid[] = "Campus7_Room3_2.4";
const char password[] = "12345678";
const char mqtt_server[] = "192.168.0.92";

WifiUtil wifi(2, 3);
WiFiEspClient espClient;
PubSubClient client(espClient);

AnalogSensor illu(A0, 0, 1023);
Led led(9);
MiniCom com;

Servo servo;
int motorPin(13);

void mqtt_init() {
    client.setServer(mqtt_server, 1883);
}

void reconnect() {
    while(!client.connected()) {
        Serial.print("Attempting MQTT connection....");

        if(client.connect("IlluEspClient")) {
            Serial.println("connected");
            client.subscribe("home/home1/illu");
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
    float i = illu.read();
    char message[10];

    dtostrf(i, 5, 2, message);
    client.publish("iot/home1/illu", message);

    Serial.println(i);
}

void setup()
{
	Serial.begin(9600);
    wifi.init(ssid, password);
    mqtt_init();
    com.setInterval(2000, publish);
    servo.attach(motorPin);
    servo.write(80);
}

void loop()
{
    if (!client.connected()) {
        reconnect();
    }

    client.loop();
    com.run();

}
