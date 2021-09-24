#define run_speed 80
void setup() {
  Serial.begin(9600);
  for(int i = 6; i < 8; i++){
    pinMode(i,OUTPUT);
  }
  //analogWrite(6, 80);
  digitalWrite(7, LOW);
}

void loop() {
  if(Serial.available()){
    Serial.print("in ");
    int input = Serial.read() - '0';
    
    Serial.println(input);
    if(input == 1){
      analogWrite(6, run_speed);
    }else if(input == 0){
      analogWrite(6, 0);
    }
    while(!Serial.available());
    while(Serial.available()){
      int trash = Serial.read();
    }
    //Serial.flush();
  }
}
