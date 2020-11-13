package com.example.usemqtt

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import kotlinx.android.synthetic.main.activity_mqtt.*

const val SUB_TOPIC = "iot/roomtemp"
const val PUB_TOPIC = "iot/wanttobe"
const val SERVER_URI = "tcp://192.168.25.3:1883"

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
            val mqttIntent = Intent(this, LightandWindowActivity::class.java)
            startActivity(mqttIntent)
        }

    }

}