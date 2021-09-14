#include <Servo.h> 

#define sL A0
#define sR A1

#define NUM_READ 10
#define usred 20
#define p 0.5

int medianL(int newVal) {
  static int buf[3];
  static byte count = 0;
  buf[count] = newVal;
  if (++count >= 3) count = 0;
  float a = buf[0];
  float b = buf[1];
  float c = buf[2];
  float middle;
  if ((a <= b) && (a <= c)) {
    middle = (b <= c) ? b : c;
  } else {
    if ((b <= a) && (b <= c)) {
      middle = (a <= c) ? a : c;
    }
    else {
      middle = (a <= b) ? a : b;
    }
  }
  return middle;
}

int runMiddleArifmOptimL(int newVal) {
  static int t = 0;
  static int vals[NUM_READ];
  static int average = 0;
  if (++t >= NUM_READ) t = 0; // перемотка t
  average -= vals[t];         // вычитаем старое
  average += newVal;          // прибавляем новое
  vals[t] = newVal;           // запоминаем в массив
  return (average / NUM_READ);
}

int medianR(int newVal) {
  static int buf[3];
  static byte count = 0;
  buf[count] = newVal;
  if (++count >= 3) count = 0;
  float a = buf[0];
  float b = buf[1];
  float c = buf[2];
  float middle;
  if ((a <= b) && (a <= c)) {
    middle = (b <= c) ? b : c;
  } else {
    if ((b <= a) && (b <= c)) {
      middle = (a <= c) ? a : c;
    }
    else {
      middle = (a <= b) ? a : b;
    }
  }
  return middle;
}

int runMiddleArifmOptimR(int newVal) {
  static int t = 0;
  static int vals[NUM_READ];
  static int average = 0;
  if (++t >= NUM_READ) t = 0; // перемотка t
  average -= vals[t];         // вычитаем старое
  average += newVal;          // прибавляем новое
  vals[t] = newVal;           // запоминаем в массив
  return (average / NUM_READ);
}

Servo rul;

void setup() {
  rul.attach(13);
  rul.write(45);
  for(int i = 6; i < 8; i++){
    pinMode(i,OUTPUT);
  }
  analogWrite(6, 150);
  digitalWrite(7, LOW);
  Serial.begin(9600);
  pinMode(sL, INPUT);
  pinMode(sR, INPUT);
  
}

void loop() {
  int dataL = analogRead(sL);
  int dataR = analogRead(sR);
//  Serial.print(dataL);
//  Serial.print("  ");
  int median_dataL = medianL(dataL);
  int median_dataR = medianR(dataR);
//  Serial.print(median_data);
  int end_sensL = runMiddleArifmOptimL(median_dataL);
  int end_sensR = runMiddleArifmOptimR(median_dataR);
//  Serial.print("  ");
//  Serial.print(end_sensL);
  int distanceL = 0;
  int distanceR = 0;
  
  for(int i = 0; i < usred; i++){
    float distL = end_sensL*0.0048828125;
    distanceL+=32*pow(distL,-1.10);
    float distR = end_sensR*0.0048828125;
    distanceR+=32*pow(distR,-1.10);
  }
  distanceL = distanceL/usred;
  distanceR = distanceR/usred;
  Serial.print(distanceL);
  Serial.print("  ");
  Serial.println(distanceR);
  int err = (distanceL - distanceR)*p;
    if(45 - err > 64){
      rul.write(64);
    }else if(45 - err < 26){
      rul.write(26);
    }else{rul.write(45 - err);}
}
