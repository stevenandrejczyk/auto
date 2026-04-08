void setup() {
  Serial.begin(9600);
}

void loop() {
  float fakeTemp = 20 + random(-50, 50) / 10.0;

  Serial.print("TEMP:");
  Serial.println(fakeTemp);

  delay(1000);
}