#pragma once
#include <Arduino.h>

class Flame{
protected:
    int pin;

public:
    Flame(int pin);
    int read();
};