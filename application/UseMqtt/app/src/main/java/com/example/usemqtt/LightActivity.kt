package com.example.usemqtt

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_light.*
import org.eclipse.paho.client.mqttv3.MqttMessage
import java.util.*
import kotlin.concurrent.timer

class LightActivity : AppCompatActivity() {
    private var timerTask: Timer? = null
    lateinit var mqttClient: Mqtt
    var manualillu = 5
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_light)
        mqttClient = Mqtt(this, SERVER_URI)
        try {
            // mqttClient.setCallback { topic, message ->}
            mqttClient.setCallback(::onReceived)
            mqttClient.connect(arrayOf<String>("home/livingroom/light"))
        } catch (e: Exception) {
            e.printStackTrace()
        }

        illuswitch.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
                // The toggle is enabled
                mqttClient.publish("home/livingroom/manualstate","1")
                manuillu()
            } else {
                // The toggle is disabled
                mqttClient.publish("home/livingroom/manualstate","0")
                timerTask?.cancel()
            }
        }
        illuup.setOnClickListener(){
            manualillu += 1
            if (manualillu>10){
                toastUp()
                manualillu = 10
            }
            curillu.text = manualillu.toString()
        }
        illudown.setOnClickListener(){
            manualillu -= 1
            if (manualillu<0){
                toastUp()
                manualillu = 0
            }
            curillu.text = manualillu.toString()
        }
    }
    fun onReceived(topic: String, message: MqttMessage) {
        // 토픽 수신 처리
        val msg = String(message.payload)
        roomillu.text = msg
    }
    fun manuillu() {
        timerTask= timer(period = 2500){
            if (manualillu>-1&&manualillu<11) {
                mqttClient.publish("home/livingroom/manual/illu", manualillu.toString())
            }
        }
    }
    fun toastUp() {
        Toast.makeText(this@LightActivity,"밝기값은 0과 10 사이여야 합니다",Toast.LENGTH_SHORT).show()
    }
}