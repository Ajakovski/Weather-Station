// =====================================================
// Паметна работна станица - Arduino DHT11 код
// Читање на температура и влага, испраќање преку Serial
// =====================================================

#include "DHT.h"

#define DHTPIN 2        // DATA пин на DHT11 поврзан на D2
#define DHTTYPE DHT 11   // Тип на сензор: DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);    // Иницијализација на Serial комуникација (9600 baud)
  dht.begin();           // Иницијализација на DHT сензорот
  Serial.println("Sistem pokrenat. Citanje na temperatura i vlaga...");
}

void loop() {
  delay(2000);  // Чекање 2 секунди помеѓу мерења (DHT11 бара мин. 1 сек)

  float t = dht.readTemperature();   // Читање на температура (°C)
  float h = dht.readHumidity();      // Читање на влага (%)

  // Проверка дали читањето е успешно
  /*if (isnan(t) || isnan(h)) {
    Serial.println("GRESKA: Neuspesno citanje od DHT senzor!");
    return;
  }*/

  // Испраќање на податоци во формат: temperatura,vlaga
  // Пример: 23.50,55.30
  Serial.print(t);
  Serial.print(",");
  Serial.println(h);

}
