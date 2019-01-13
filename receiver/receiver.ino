/*
 * 美嘉欣 2.4G 无线遥控接收程序
 * 
 * RX_Address：mjsss
 * RC_ChannelList: 0x25, 0x2A, 0x32, 0x2C, 0x14, 0x27, 0x36, 0x34,
 *                 0x1C, 0x17, 0x11, 0x1A, 0x35, 0x24, 0x28, 0x18；
 * CRC: 2 Bytes
 * AutoAck: Disable
 * DataRate: 1MBPS
 * PayloadSize: 16 Bytes 
 * 
*/

#include <nRF24L01.h>
#include <printf.h>
#include <RF24.h>
#include <RF24_config.h>

#include <stdio.h>  // for sprintf() call

// CE:7 CSN:8
RF24 radio(7, 8);

// LED
byte brightness = 0;

// RX_Address
const byte rxAddr[] = "mjsss";

// RX_ChannelList
const byte rxChannelList[] = {0x25, 0x2A, 0x32, 0x2C, 0x14, 0x27, 0x36, 0x34,
                              0x1C, 0x17, 0x11, 0x1A, 0x35, 0x24, 0x28, 0x18};

char serial_tx_buffer[30];

void setup()
{
  //while (!Serial);
  Serial.begin(1000000);
  printf_begin();

  pinMode(LED_BUILTIN, OUTPUT);
    
  // Receive Interrupt
  attachInterrupt(digitalPinToInterrupt(2), Receiver, FALLING);
  
  radio.begin();                    
  
  radio.setCRCLength(RF24_CRC_16); // CRC-2 bytes
  
  radio.powerUp();                 // PWR_UP & PRIM_RX
  
  radio.setAutoAck(false);         // Disable auto Acknowlage
  
  radio.setChannel(0x25);          // chanel - 0x25(start Channel)
  
  radio.setDataRate(RF24_1MBPS);   // date rate - 1M
 
  radio.setPayloadSize(16);        // payload width - 16
  
  radio.openReadingPipe(0, rxAddr);// open read pip
  
  radio.startListening();          // start listening
  
  //radio.printDetails();
}

void loop()
{
  analogWrite(13, brightness);
  delay(100);
}

void Receiver()
{
  static char times = 0;
  static byte nextChannel = 0;
  byte SUM = 0x00;
  
  if(radio.available())
  {
    byte data[16] = {0};
    radio.read(&data, sizeof(data));

    brightness = data[0];
    
    sprintf(serial_tx_buffer, "H%d %d %d %d %dE\n",\
            data[0],                // throttle
            convertValue(data[1]),  // rotate
            convertValue(data[2]),  // forward-back
            convertValue(data[3]),  // left-right
            data[14]);              // button
            
    Serial.print(serial_tx_buffer);
    Serial.flush();           
    times++;
  }
  else 
  {
    times = 0;
    nextChannel = 0;
  }
  if(times >= 1)
  {
    times = 0;
    nextChannel++;
    if(nextChannel == sizeof(rxChannelList))
    {
      nextChannel = 0;
    }
    // radio stop
    radio.stopListening();
    // change channel
    radio.setChannel(rxChannelList[nextChannel]);
    // radio start
    radio.startListening();
  }
}

char convertValue(byte value)
{
  if(value & 0x80)
    return (value & 0x7F);
  else
    return -value; 
}



