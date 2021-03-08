void sweep() {

//Sweep Parameters
long start_angle = 60; //Starting angle of depression (deg)
int end_distance = 5; //Largest ring radius (m)
float sensor_height = 1.2; //approximate height of the lidar - best to have this higher than it actually is (m)
float distance_between_points = 10; //Space between rings (cm)

int number_of_rings = 1;//(end_distance-sensor_height*cos(start_angle*PI/180))*100/distance_between_points; //number of rings to scan. Can adjust the last number to adjust spacing between rings
float L = sensor_height/tan(PI/180*start_angle);

//Bring sensor down to the set angle of depression
  digitalWrite(PD,LOW);
  while(pitchPos <= start_angle*motorSteps/360) {
    digitalWrite(PS,HIGH);
    delayMicroseconds(Speed);
    digitalWrite(PS,LOW);
    delayMicroseconds(Speed);
    pitchPos++;
  }
   scanFile = SD.open(fileName, FILE_WRITE);
   scanFile.print("SCAN,");
   scanFile.println(pos);
   scanFile.close();

//The scanning loop
digitalWrite(PD,HIGH);
  float steps_to_pitch = start_angle;
  for (int j = 1; j <= number_of_rings; j++) {

    //Pitching up to the next ring
    long steps_to_pitch = motorSteps/2*atan(sensor_height/L)/PI; 
    L = L + distance_between_points/100;
    
    while(pitchPos > steps_to_pitch) {
      digitalWrite(PS,HIGH);
      delayMicroseconds(Speed);
      digitalWrite(PS,LOW);
      delayMicroseconds(Speed);
      pitchPos--;
    }
 
   //Sweeping
   float alpha = steps_to_pitch*360/motorSteps*PI/180;
   long steps_to_yaw = motorSteps*asin(distance_between_points/100*sin(alpha)/(2*sensor_height))/PI;
   int i = steps_to_yaw;
   

   
   digitalWrite(YD,HIGH);
   for(int k = 0; k < motorSteps; k++) {
    if (i == steps_to_yaw) {
      scanFile = SD.open(fileName, FILE_WRITE);
      myLidarLite.waitForBusy();
      myLidarLite.takeRange();
//      Serial.print(yawPos);
//      Serial.print(",");
//      Serial.print(pitchPos);
//      Serial.print(",");
//      myLidarLite.waitForBusy();
//      Serial.println(myLidarLite.readDistance());
      scanFile.print(yawPos);
      scanFile.print(",");
      scanFile.print(pitchPos);
      scanFile.print(",");
      myLidarLite.waitForBusy();
      scanFile.println(myLidarLite.readDistance());
      scanFile.close();
      i = 0;
    }
    digitalWrite(YS,HIGH);
    delayMicroseconds(Speed);
    digitalWrite(YS,LOW);
    delayMicroseconds(Speed);
    yawPos++;   
    i++;

   if (yawPos >= 3200) {
    yawPos = yawPos - 3200;
   }
  }
  }
  

}
