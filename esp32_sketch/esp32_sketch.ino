const int soilPin = 34;  // Analog pin

void setup() {
  Serial.begin(115200);
}

void loop() {
  int raw = analogRead(soilPin);
  float percent = map(raw, 4095, 1600, 0, 100);  // Adjust range as needed
  Serial.print("Raw: ");
  Serial.print(raw);
  Serial.print(" → Moisture: ");
  Serial.print(percent);
  Serial.println("%");
  delay(2000);
}
