package com.example.usemqtt

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import kotlinx.android.synthetic.main.activity_mqtt.*
import org.eclipse.paho.client.mqttv3.MqttMessage

const val SUB_TOPIC = "iot/roomtemp"
const val PUB_TOPIC = "iot/wanttobe"
const val SERVER_URI = "tcp://192.168.0.94:1883"

class MainActivity : AppCompatActivity() {
    val TAG = "MqttActivity"
    lateinit var mqttClient: Mqtt
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_mqtt)

        airconmod.setOnClickListener{
            val mqttIntent = Intent(this, AirconActivity::class.java)
            startActivity(mqttIntent)
        }

        lightmod.setOnClickListener{
            val mqttIntent = Intent(this, LightActivity::class.java)
            startActivity(mqttIntent)
        }

    }

}