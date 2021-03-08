 void track() {
//x 0-320, y 0-240

//Serial.print("yaw: ");
//Serial.print(yaw);
//Serial.print(", pitch: ");
//Serial.print(pitch);

if (yaw>=162) {
  digitalWrite(YD,HIGH);
  digitalWrite(YS,HIGH);
  yawPos++;
}
if (yaw<=158) {
  digitalWrite(YD,LOW);
  digitalWrite(YS,HIGH);
  yawPos--;
}
if (pitch>=122) {
  digitalWrite(PD,LOW);
  digitalWrite(PS,HIGH);
  pitchPos++;
}
if (pitch<=118) {
  digitalWrite(PD,HIGH);
  digitalWrite(PS,HIGH);
  pitchPos--;
}

delayMicroseconds(Speed);
digitalWrite(YS,LOW);
digitalWrite(PS,LOW);
delayMicroseconds(Speed);

//Serial.print(" yaw: ");
//Serial.print(yawSteps);
//Serial.print(", pitch: ");
//Serial.print(pitchSteps);

  //roll over step count
  if (yawPos >= 3200) {
    yawPos = yawPos - 3200;
  }
  if (yawPos <= -1) {
    yawPos = yawPos + 3200;
  }
}
