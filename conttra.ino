float anlg1;
float anlg2;
int mil;
unsigned long mils;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  anlg1 = analogRead(0);
  anlg2 = analogRead(1);
  mils = millis();
  Serial.print(anlg1);
  Serial.print(";");
  Serial.print(anlg2);
  Serial.print(";");
  Serial.print(mils);
  Serial.println("");
  int timeout = 0;
  char command = 0;
  while (Serial.available()==0) {
    if (++timeout>10000){
      break;
    }
   }
  if (Serial.available()>0){
    command = Serial.read();
  }
  timeout = 0; // got a char so reset timeout
  switch (command) {
    case 1:
    digitalWrite(13, HIGH);
    break;
    case 0:
    digitalWrite(13, LOW);
    break;
    default:
    digitalWrite(13, LOW);
    break;
  }
}