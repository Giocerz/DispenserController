#include "HX711.h"
#include <Servo.h>

const int DOUT=A1;
const int CLK=A0;

HX711 balanza;
Servo servoMotor;

float y = 0.0, e = 0.0, r = 0.0;

int status = 0, runState = 0, angle = 0;
unsigned long time1 = 0, time2 = 0;
char comando[3];

void setup() {
  Serial.begin(9600);
  servoMotor.attach(9);
  servoMotor.write(0);
  balanza.begin(DOUT, CLK);
  balanza.set_scale(2122.12508);
}

void loop() {
  if(comando[0] == 'i' && comando[1] == 'n'){
    runState = 1;
    r = (float)comando[2];
    control();
    servoMotor.write(0);
    if(e <= 0.0){
      Serial.println('c');
    }
    comando[0] = ' ';
  }else if(comando[0] == 't'){
    balanza.tare(10);
    Serial.println('T');
    comando[0] = ' ';
  }
}

void serialEvent(){
  if (Serial.available()) {
    Serial.readBytes(comando, 3);
  }
}

void control(){
  while(1){
    if (Serial.available()) {
      Serial.readBytes(comando, 3);
      if(comando[0] == 'd'){
        break;
      }
    } 
    time1 = millis();
    y = balanza.get_units();
    Serial.print('p');
    Serial.println(y,3);
    e = r - y;
    if(e <= 0.0){
      break;    
    }
    e = e*1.24;
    angle = map(e,0.0,100.0,40,180);
    servoMotor.write(angle);
    while(millis() - time1 < 300);
  }    
}
