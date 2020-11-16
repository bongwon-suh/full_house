package com.example.usemqtt

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import kotlinx.android.synthetic.main.activity_aircon.*
import kotlinx.android.synthetic.main.activity_mqtt.*
import java.util.*
import kotlin.concurrent.schedule

const val SERVER_URI = "tcp://192.168.0.92:1883"

class MainActivity : AppCompatActivity() {
    private var timerTask: Timer? = null
    lateinit var mqttClient: Mqtt

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_mqtt)
        mqttClient = Mqtt(this, SERVER_URI)
        try {
        // mqttClient.setCallback { topic, message ->}
            mqttClient.connect(arrayOf<String>("home"))
        } catch (e: Exception) {
            e.printStackTrace()
        }

        entranceswitch.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
            // The toggle is enabled
                mqttClient.publish("home/auto","0")
                Timer().schedule(100){
                    mqttClient.publish("home/entrance_state/door","1" )
                }
                Timer().schedule(2000){
                    mqttClient.publish("home/auto","1" )
                }
            } else {
            // The toggle is disabled
                mqttClient.publish("home/auto","0")
                Timer().schedule(100){
                    mqttClient.publish("home/entrance_state/door","0" )
                }
                Timer().schedule(2000){
                    mqttClient.publish("home/auto","1" )
                }
            }
        }

        garageswitch.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
            // The toggle is enabled
                mqttClient.publish("home/auto","0")
                Timer().schedule(100){
                    mqttClient.publish("home/entrance_state/garage_door","1" )
                }
                Timer().schedule(2000){
                    mqttClient.publish("home/auto","1" )
                }
            } else {
            // The toggle is disabled
                mqttClient.publish("home/auto","0")
                Timer().schedule(100){
                    mqttClient.publish("home/entrance_state/garage_door","0" )
                }
                Timer().schedule(2000){
                    mqttClient.publish("home/auto","1" )
                }
            }
        }

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