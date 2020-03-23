#include <MFRC522.h>
#include <SPI.h>


int rst_pin = 9;
int ss_pin = 10;


MFRC522 rfid(ss_pin, rst_pin);

byte ID[4] = {64,22,112,196};
 

void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();
  
}

void loop() {
  // put your main code here, to run repeatedly:

  if ( !rfid.PICC_IsNewCardPresent() )
    return;
  
  if ( !rfid.PICC_ReadCardSerial() )
    return;

  if ( rfid.uid.uidByte[0] == ID[0] &&
    rfid.uid.uidByte[1] == ID[1] &&
    rfid.uid.uidByte[2] == ID[2] &&
    rfid.uid.uidByte[3] == ID[3] ) { 
      Serial.println("acil susam acil");
    }
  else {
      Serial.println("sanmiyorum girebilecegini");
      ID_Number();
  }
  rfid.PICC_HaltA(); 
}


void ID_Number(){
  Serial.print("ID Number: ");
  for(int i = 0; i < 4; i++){
    Serial.print(rfid.uid.uidByte[i]);
    Serial.print(" ");
  }
  Serial.println("");
}
