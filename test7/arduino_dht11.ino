#include "DHT.h"

#define DHT_PIN 2
#define DHT_TYPE 11

DHT dht(DHT_PIN,DHT_TYPE);

void setup(){
    Serial.begin(9600);
    dht.begin();
}

void loop(){
    delay(2000);
    float t=dht.readTemperature();
    float h=dht.readHumidity();

    if(isnan(t) || isnan(h)){
        Serial.print("Greska pri citanje od dht senzor");
        return;
    }
    if(t<80 && t>-40 && h<100 && h>0){
        Serial.print(t);
        Serial.print(",");
        Serial.println(h);}
    else{
        Serial.println("Greska pri odcituvanje");
        return;
    }
}