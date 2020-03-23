int Sensor = 0;
int Detection = 0;

void setup() {
  Serial.begin(9600);
  
}

void loop() {

  Detection = analogRead(Sensor);


  Serial.println(Detection);
  delay(100);

}
