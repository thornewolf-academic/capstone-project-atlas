void Startup() {
  int k = 0;
  int distance;
  while (k == 0) {
    myLidarLite.waitForBusy();
    myLidarLite.takeRange();
    myLidarLite.waitForBusy(); //may be able to remove this for more speed. have not tested
    distance = myLidarLite.readDistance();
    if (distance != 0) {
      digitalWrite(PS,HIGH);
      delayMicroseconds(Speed);
      digitalWrite(PS,LOW);
      delayMicroseconds(Speed);
    }
    if (distance == 0) {
      k = 1;
    }
  }
  digitalWrite(PD,HIGH);
  
  for (int j = 0; j<635; j++) { // is level
    digitalWrite(PS,HIGH);
    delayMicroseconds(Speed);
    digitalWrite(PS,LOW);
    delayMicroseconds(Speed);
  }

}
