void track() {
//x 0-320, y 0-240
int yawSteps = 0;
int pitchSteps = 0;
int i = 0;
int j = 0;

int Yp = 20;
int Pp = 20;

if (yaw>160) {
  yawSteps = (yaw-160)/Yp+1;
  digitalWrite(YD,HIGH);
  yawPos = yawPos+yawSteps;
}
if (yaw<160) {
  yawSteps = (160-yaw)/Yp+1;
  digitalWrite(YD,LOW);
  yawPos = yawPos-yawSteps;
}
if (pitch>120) {
  pitchSteps = (pitch-120)/Pp+1;
  digitalWrite(PD,LOW);
  pitchPos = pitchPos+pitchSteps;
}
if (pitch<120) {
  pitchSteps = (120-pitch)/Pp+1;
  digitalWrite(PD,HIGH);
  pitchPos = pitchPos-pitchSteps;
}

while (i < yawSteps || j < pitchSteps){
  if (i < yawSteps) {
    digitalWrite(YS,HIGH);
    i++;
  }
  if (j < pitchSteps) {
    digitalWrite(PS,HIGH);
    j++;
  }
  delayMicroseconds(Speed);
  digitalWrite(YS,LOW);
  digitalWrite(PS,LOW);
  delayMicroseconds(Speed);
}

//Serial.print(yaw);
//Serial.print(",");
//Serial.println(pitch);

yawPos = yawPos % 3200;
}
