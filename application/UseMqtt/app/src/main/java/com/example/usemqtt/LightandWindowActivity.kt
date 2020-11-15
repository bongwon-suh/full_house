package com.example.usemqtt

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.SeekBar
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_light.*
import org.eclipse.paho.client.mqttv3.MqttMessage
import java.util.*
import kotlin.concurrent.schedule
import kotlin.concurrent.timer



class LightandWindowActivity : AppCompatActivity() {
    private var timerTask: Timer? = null
    lateinit var mqttClient: Mqtt
    var manualillu = 0
    var manualwindo = 0
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_light)
        mqttClient = Mqtt(this, SERVER_URI)
        try {
            // mqttClient.setCallback { topic, message ->}
            mqttClient.setCallback(::onReceived)
            mqttClient.connect(arrayOf<String>("home/livingroom/illu"))
        } catch (e: Exception) {
            e.printStackTrace()
        }

        activeswitch2.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked) {
                // The toggle is enabled
                mqttClient.publish("home/livingroom/manualstate","1")
                manuactive()
            } else {
                // The toggle is disabled
                mqttClient.publish("home/livingroom/manualstate","0")
                timerTask?.cancel()
            }
        }
        illuup.setOnClickListener(){
            manualillu += 1
            if (manualillu>30){
                toastlightUp()
                manualillu = 30
            }
            curillu.text = manualillu.toString()
        }
        illudown.setOnClickListener(){
            manualillu -= 1
            if (manualillu<0){
                toastlightUp()
                manualillu = 0
            }
            curillu.text = manualillu.toString()
        }
        illubar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener{
            override fun onProgressChanged(seekBar: SeekBar, i: Int, b: Boolean) {
                // Display the current progress of SeekBar
                manualillu = i
                curillu.text = manualillu.toString()
            }
            override fun onStartTrackingTouch(seekBar: SeekBar?) {
            }

            override fun onStopTrackingTouch(seekBar: SeekBar?) {
            }
        })

        windoup.setOnClickListener(){
            manualwindo += 1
            if (manualwindo>30){
                toastwindoUp()
                manualwindo = 30
            }
            curwindo.text = manualwindo.toString()
        }
        windodown.setOnClickListener(){
            manualwindo -= 1
            if (manualwindo<0){
                toastwindoUp()
                manualwindo = 0
            }
            curwindo.text = manualwindo.toString()
        }
        windobar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener{
            override fun onProgressChanged(seekBar: SeekBar, i: Int, b: Boolean) {
                // Display the current progress of SeekBar
                manualwindo = i
                curwindo.text = manualwindo.toString()
            }
            override fun onStartTrackingTouch(seekBar: SeekBar?) {
            }

            override fun onStopTrackingTouch(seekBar: SeekBar?) {
            }
        })
    }
    fun onReceived(topic: String, message: MqttMessage) {
        // 토픽 수신 처리
        val msg = String(message.payload)
        roomillu.text = msg
    }
    fun manuactive() {
        timerTask=timer(period = 2500){
            mqttClient.publish("home/livingroom/manual/illu", (manualillu.toFloat()/30).toString() )
            Timer().schedule(1000){
                mqttClient.publish("home/livingroom/manual/windo", ((manualwindo.toFloat()/15)-1).toString() )
            }

        }
    }
    fun toastlightUp() {
        Toast.makeText(this@LightandWindowActivity,"밝기값은 0과 30 사이여야 합니다",Toast.LENGTH_SHORT).show()
    }
    fun toastwindoUp() {
        Toast.makeText(this@LightandWindowActivity,"창문의 열린 정도는 0과 30 사이여야 합니다",Toast.LENGTH_SHORT).show()
    }

    override fun onDestroy() {
        super.onDestroy()
        timerTask?.cancel()
    }
}
