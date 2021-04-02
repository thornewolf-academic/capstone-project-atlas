
void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (camera.available() > 0 && newData == false) {
        rc = camera.read();
        //Serial.println(rc);
        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts


    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");      // get the first part - the string
    flag = atoi(strtokIndx);
 
    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    yaw = atoi(strtokIndx);     

    strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
    pitch = atoi(strtokIndx);  
}

//============

void showParsedData() {
    Serial.print("Flag ");
    Serial.print(flag);
    Serial.print(", Yaw ");
    Serial.print(yaw);
    Serial.print(", Pitch ");
    Serial.println(pitch);
}
