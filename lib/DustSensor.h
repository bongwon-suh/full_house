#pragma once
#include <Arduino.h>

class DustSensor
{
protected:
    int PIN;
    long duration;
    long start_time;
    long sampletime_ms = 2000;
    long lowpulseoccupancy = 0;
    float ratio = 0;
    float concentration = 0;
    int ugm3 = 0;

public:
    DustSensor(int PIN, long start_time = 0);
    int getDust();
};
