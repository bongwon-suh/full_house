package com.example.usemqtt

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_aircon.*
import org.eclipse.paho.client.mqttv3.MqttMessage
import java.util.*
import kotlin.concurrent.timer

class AirconActivity : AppCompatActivity() {
    private var timerTask: Timer? = null
    lateinit var mqttClient: Mqtt
    var manualtemp = 27
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_aircon)
        mqttClient = Mqtt(this, SERVER_URI)
        try {
            // mqttClient.setCallback { topic, message ->}
            mqttClient.setCallback(::onReceived)
            mqttClient.connect(arrayOf<String>("home/livingroom/temp"))
        } catch (e: Exception) {
            e.printStackTrace()
        }

        tempswitch.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
                // The toggle is enabled
                mqttClient.publish("home/livingroom/manualstate","1")
                manutemp()
            } else {
                // The toggle is disabled
                mqttClient.publish("home/livingroom/manualstate","0")
                timerTask?.cancel()
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

    fun manutemp() {
        timerTask=timer(period = 2500){
            mqttClient.publish("home/livingroom/manual/temp", manualtemp.toString() )
        }
    }
}