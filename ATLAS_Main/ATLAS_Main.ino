#include <stdint.h>
#include <Wire.h>
#include <LIDARLite_v3HP.h>
LIDARLite_v3HP myLidarLite;
#define FAST_I2C
#include <SPI.h>
#include <SD.h>

String fileName = "scan1.txt";

//Motor code variables
const int YS = A3; //defining pins
const int YD = A2;
const int PS = A1; //pitch step pin
const int PD = A0; //pitch direction pin
const int button = 7;

int motorSteps = 3200;       //no. motor steps for 1 rotation
unsigned long Speed = 500000 / (motorSteps/3);   //to change axis motor speed. number is hz


int buttonState = 0;
int yaw = 160;
int pitch = 120;
int yawPos = 0;
int pitchPos = 0;
int flag = 0;
float dist1 = 0;
float dist2 = 0;
int ontarget = 0;
int pos = 1;
int searchDelay = 0;

//Serial data system variables
const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars]; 
boolean newData = false; 
const int chipSelect = 10; //for SD card
File scanFile;


void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
  pinMode(YS, OUTPUT);
  pinMode(YD, OUTPUT);
  pinMode(PS, OUTPUT);
  pinMode(PD, OUTPUT);
  pinMode(button, INPUT_PULLUP);
  digitalWrite(YS, LOW);
  digitalWrite(PS, LOW);

  // Initialize Arduino I2C (for communication to LidarLite)
  Wire.begin();
#ifdef FAST_I2C
#if ARDUINO >= 157
  Wire.setClock(400000UL); // Set I2C frequency to 400kHz (for Arduino Due)
#else
  TWBR = ((F_CPU / 400000UL) - 16) / 2; // Set I2C frequency to 400kHz
#endif
#endif

  // Configure the LidarLite internal parameters so as to lend itself to
  // various modes of operation by altering 'configure' input integer to
  // anything in the range of 0 to 5. See LIDARLite_v3HP.cpp for details.
  myLidarLite.configure(2);

  delay(3000);

  //Checks to ensure an SD card is inserted
//  if (!SD.begin(chipSelect)) {
//    Serial.println("Card failed, or not present");
//    // don't do anything more:
//    while (1);
//  }
  Serial.println("sd card ok");
  Startup();
  delay(1000);
    scanFile = SD.open(fileName, FILE_WRITE);
    scanFile.print("LOCALIZE,");
    scanFile.println(pos);
    scanFile.close();
    Serial.print("LOCALIZE,");
    Serial.println(pos);
}

void loop() {

if (digitalRead(button) == 0) {
  buttonState = 1;
}


while (buttonState == 1) {
// Parses the data coming in
  recvWithStartEndMarkers();
  if (newData == true) {
    strcpy(tempChars, receivedChars);
    // this temporary copy is necessary to protect the original data
    //   because strtok() used in parseData() replaces the commas with \0
    parseData();
    //showParsedData();
    newData = false;
    
    if ((flag == 0) || (flag == 1 && dist1 != 0) || (flag == 2 && dist2 !=0)) {
      if (searchDelay == 1) {
        delay(500);
        searchDelay = 0;
      }
      else {
        for (int p = 0; p < 10; p++) {
          search();
        }
      }
    }
  
    if (flag == 1 && dist1 == 0) {
      int searchDelay = 1;
      track();
      
      if ((pitch == 120) && (yaw == 160)) {
        ontarget++;
        //Serial.println(ontarget);
      }
      if ((pitch != 120) || (yaw != 160)) {
        ontarget = 0;
      }
      if (ontarget == 200) {
        dist1 = lidar();
        int PS1 = pitchPos;
        int YS1 = yawPos;
        ontarget = 0;
        
        Serial.print("1,");
        Serial.print(YS1);
        Serial.print(",");
        Serial.print(PS1);
        Serial.print(",");
        Serial.println(dist1);
    
        scanFile = SD.open(fileName, FILE_WRITE);
        scanFile.print("1,");
        scanFile.print(YS1);
        scanFile.print(",");
        scanFile.print(PS1);
        scanFile.print(",");
        scanFile.println(dist1);
        scanFile.close();
      }
    }
    
    if (flag == 2 && dist2 == 0) {
      track();
      int searchDelay = 1;
      
      if (((pitch == 120) && (yaw == 160))) {
        ontarget++;
      }
      if ((pitch != 120) || (yaw != 160)) {
        ontarget = 0;
      }
      if (ontarget == 200) {
        dist2 = lidar();
        int PS2 = pitchPos;
        int YS2 = yawPos;
        ontarget = 0;
        
        Serial.print("2,");
        Serial.print(YS2);
        Serial.print(",");
        Serial.print(PS2);
        Serial.print(",");
        Serial.println(dist2);
    
        scanFile = SD.open(fileName, FILE_WRITE);
        scanFile.print("2,");
        scanFile.print(YS2);
        scanFile.print(",");
        scanFile.print(PS2);
        scanFile.print(",");
        scanFile.println(dist2);
        scanFile.close();
      }
    }
  }
  
if (dist1 != 0 && dist2 != 0) {
  search();
  dist1 = 0;
  dist2 = 0;
  //Serial.print("SCAN,");
  //Serial.println(pos);
  //Serial.println("0,0,0");
  pos++;
  //Serial.print("LOCALIZE,");
  //Serial.println(pos);
  sweep();
  scanFile = SD.open(fileName, FILE_WRITE);
  scanFile.print("LOCALIZE,");
  scanFile.println(pos);
  scanFile.close();
  search();
  buttonState = 0;
}


  //roll over step count
  yawPos = yawPos % 3200;
}
}

// call lidar() to get average of 10 lidar measurements
int lidar() {
  int i = 0;
  float distance = 0;
  while (i < 10) {
    myLidarLite.waitForBusy();
    myLidarLite.takeRange();
    myLidarLite.waitForBusy(); //may be able to remove this for more speed. have not tested
    distance = distance + myLidarLite.readDistance();
    //Serial.println(distance);
    i++;
  }
  distance = distance / 10;
  return distance;
}
