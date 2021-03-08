
void search() {     
  //Serial.println(pitchPos); 
      while (pitchPos != 0) {
        if (pitchPos > 0) {
          digitalWrite(PD,HIGH);
          pitchPos--;
        }
        if (pitchPos < 0) {
          digitalWrite(PD,LOW);
          pitchPos++;
        }
        digitalWrite(PS,HIGH);
        delayMicroseconds(Speed*6);
        digitalWrite(PS,LOW);
        delayMicroseconds(Speed*6);
      }

       if (pitchPos == 0) {
        //step motor
        digitalWrite(YD,HIGH);
        digitalWrite(YS,HIGH);
        delayMicroseconds(Speed*3);
        digitalWrite(YS,LOW);
        delayMicroseconds(Speed*3);
        yawPos++;
      }
}
