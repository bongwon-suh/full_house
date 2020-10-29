#include "DustSensor.h"
DustSensor::DustSensor(int PIN, long start_time) : PIN(PIN), start_time(start_time)
{
    start_time = millis();
    pinMode(PIN, INPUT);
}

int DustSensor::getDust()
{
    duration = pulseIn(PIN, LOW);
    lowpulseoccupancy += duration;
    if ((millis() - start_time) > sampletime_ms)
    {
        ratio = lowpulseoccupancy / (sampletime_ms * 10.0);
        concentration = 1.1 * pow(ratio, 3) - 3.8 * pow(ratio, 2) + 520 * ratio + 0.62;
        ugm3 = concentration * 100 / 13000;
        lowpulseoccupancy = 0;
        start_time = millis();
    }

    return ugm3;
}
