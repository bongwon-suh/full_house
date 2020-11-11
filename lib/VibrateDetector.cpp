#include "VibrateDetector.h"


VibrateDetector::VibrateDetector(int din,int Aout):din(din),Aout(Aout){
    pinMode(din, INPUT);
    
}
int VibrateDetector::read(){
    int value = analogRead(Aout);
    value = 1023-value;
    return value;
}