package com.example.usemqtt

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_aircon.*
import org.eclipse.paho.client.mqttv3.MqttMessage
import kotlin.concurrent.timer


class AirconActivity : AppCompatActivity() {
    private var isRunning = false
    lateinit var mqttClient: Mqtt
    var manualtemp = 27
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_aircon)
        mqttClient = Mqtt(this, SERVER_URI)
        try {
            // mqttClient.setCallback { topic, message ->}
            mqttClient.setCallback(::onReceived)
            mqttClient.connect(arrayOf<String>(SUB_TOPIC))
        } catch (e: Exception) {
            e.printStackTrace()
        }

        switch2.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
                // The toggle is enabled
                isRunning = !isRunning
                if(isRunning) {
                    manualmode()
                    manuillu()
                }
            } else {
                // The toggle is disabled
            }
        }
        hitup.setOnClickListener(){
            manualtemp += 1
            curtemp.text = manualtemp.toString()
        }
        hitdown.setOnClickListener(){
            manualtemp -= 1
            curtemp.text = manualtemp.toString()
        }

    }

    fun onReceived(topic: String, message: MqttMessage) {
        // 토픽 수신 처리
        val msg = String(message.payload)
        roomtemp.text = msg
    }

    fun manualmode() {
        timer(period = 5000){
            mqttClient.publish("home/livingroom/manualstate","1")
        }
    }
    fun manuillu() {
        timer(period = 5000){
            mqttClient.publish("home/livingroom/manual/light", manualtemp.toString() )
        }
    }
}