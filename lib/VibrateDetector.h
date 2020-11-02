#pragma once
#include <Arduino.h>

class VibrateDetector{
protected:
    int din;
    int Aout;
public:
    VibrateDetector(int din, int Aout);
    int read();
};