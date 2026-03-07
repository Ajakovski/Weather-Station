#include "DHT.h"

#define DHT_PIN 2
#define DHT_TYPE 11

DHT dht(DHT_PIN, DHT_TYPE);

void setup(){
    Serial.begin(9600);
    dht.begin();
}

void loop(){
    delay(2000);
    float t=dht.readTemperature();
    float h=dht.readHumidity();

    if(isnan(t) || isnan(h)){
        Serial.println("Greska: Neuspesno citanje od DHT senzor!");
        return;
    }

    Serial.print(t);
    Serail.print(",");
    Serial.println(h);
}