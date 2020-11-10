package com.example.usemqtt

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import kotlinx.android.synthetic.main.activity_aircon.*
import kotlinx.android.synthetic.main.activity_light.*
import org.eclipse.paho.client.mqttv3.MqttMessage

class LightActivity : AppCompatActivity() {
    lateinit var mqttClient: Mqtt
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_light)
        mqttClient = Mqtt(this, SERVER_URI)
        try {
            // mqttClient.setCallback { topic, message ->}
            mqttClient.setCallback(::onReceived)
            mqttClient.connect(arrayOf<String>(SUB_TOPIC))
        } catch (e: Exception) {
            e.printStackTrace()
        }
        lightup.setOnClickListener {
            lightup()
        }
    }
    fun onReceived(topic: String, message: MqttMessage) {
        // 토픽 수신 처리
        val msg = String(message.payload)
        roomtemp.text = msg
    }
    fun lightup() {
        mqttClient.publish(PUB_TOPIC, "1")
    }
}