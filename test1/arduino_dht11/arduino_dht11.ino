#include "DHT.h"

#define DHTPIN 2        
#define DHTTYPE DHT11   

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);    
  dht.begin();           
  Serial.println("Sistem pokrenat. Citanje na temperatura i vlaga...");
}

void loop() {
  delay(2000); 

  float t = dht.readTemperature();  
  float h = dht.readHumidity();      

  Serial.print(t);
  Serial.print(",");
  Serial.println(h);

}