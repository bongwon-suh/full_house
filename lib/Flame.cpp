#include "Flame.h"

Flame::Flame(int pin) : pin(pin){
    pinMode(pin, INPUT);
}

int Flame::read(){
    return digitalRead(pin);
}