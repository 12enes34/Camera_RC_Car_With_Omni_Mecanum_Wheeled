#include <WiFi.h>
#include <WiFiUdp.h>
#include "pitches.h"

// Wi-Fi ayarları
const char* ssid = "Tulpar";
const char* password = "12345687";

// UDP için ayarlar
WiFiUDP udp;
const unsigned int localUdpPort = 8888;  // UDP portu
char incomingPacket[255];  // Gelen UDP paketi

// Right Engine Controller pinout
#define Front_Left_PWM 6
#define Front_Right_PWM 1
#define Front_Left_in1 5
#define Front_Left_in2 4
#define Front_Right_in3 2
#define Front_Right_in4 3

// Left Engine Controller pinout
#define Behind_Left_PWM 8
#define Behind_Right_PWM 13
#define Behind_Left_in1 9
#define Behind_Left_in2 10
#define Behind_Right_in3 12
#define Behind_Right_in4 11

// Buzzer pinout
int buzzerPin = 7;

// Buzzer melody
int melody[] = { NOTE_C5, NOTE_G4, NOTE_G4, NOTE_A4, NOTE_G4, 0, NOTE_B4, NOTE_C5 };
int noteDurations[] = { 4, 8, 8, 4, 4, 4, 4, 4 };

void setup() {
  Serial.begin(115200);
  // Wi-Fi bağlantısını başlat
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println("WiFi connected");

  // IP adresini yazdır
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // UDP başlat
  udp.begin(localUdpPort);
  Serial.printf("UDP listening on port %d\n", localUdpPort);

  // Motor pinlerini ayarla
  pinMode(Front_Left_PWM, OUTPUT);
  pinMode(Front_Left_in1, OUTPUT);
  pinMode(Front_Left_in2, OUTPUT);
  pinMode(Front_Right_PWM, OUTPUT);
  pinMode(Front_Right_in3, OUTPUT);
  pinMode(Front_Right_in4, OUTPUT);
  pinMode(Behind_Left_PWM, OUTPUT);
  pinMode(Behind_Left_in1, OUTPUT);
  pinMode(Behind_Left_in2, OUTPUT);
  pinMode(Behind_Right_PWM, OUTPUT);
  pinMode(Behind_Right_in3, OUTPUT);
  pinMode(Behind_Right_in4, OUTPUT);
}

void loop() {
  // Gelen UDP paketlerini kontrol et
  int packetSize = udp.parsePacket();
  if (packetSize) {
    // Paketi al
    int n = udp.read(incomingPacket, 255);
    incomingPacket[n] = 0;  // Null terminator ekle
    Serial.printf("Received UDP packet: %s\n", incomingPacket);

    // Komutu işleme
    processCommand(String(incomingPacket));
  }
}

// Komut işleme fonksiyonu
void processCommand(String command) {
  command.trim();
  // Komutları işleme
  if (command.startsWith("controll")) {
    int comma1 = command.indexOf(',');
    int comma2 = command.indexOf(',', comma1 + 1);
    int comma3 = command.indexOf(',', comma2 + 1);
    int comma4 = command.indexOf(',', comma3 + 1);
    int comma5 = command.indexOf(',', comma4 + 1);
    int comma6 = command.indexOf(',', comma5 + 1);
    int comma7 = command.indexOf(',', comma6 + 1);
    int comma8 = command.indexOf(',', comma7 + 1);

    if (comma1 != -1 && comma2 != -1 && comma3 != -1 && comma4 != -1 && comma5 != -1 && comma6 != -1 && comma7 != -1 && comma8 != -1) {
      int FrontLeftPWM = command.substring(comma1 + 1, comma2).toInt();
      int FrontLeftRot = command.substring(comma2 + 1, comma3).toInt();
      int FrontRightPWM = command.substring(comma3 + 1, comma4).toInt();
      int FrontRightRot = command.substring(comma4 + 1, comma5).toInt();
      int BehindLeftPWM = command.substring(comma5 + 1, comma6).toInt();
      int BehindLeftRot = command.substring(comma6 + 1, comma7).toInt();
      int BehindRightPWM = command.substring(comma7 + 1, comma8).toInt();
      int BehindRightRot = command.substring(comma8 + 1).toInt();

      controll(FrontLeftPWM, FrontLeftRot, FrontRightPWM, FrontRightRot, BehindLeftPWM, BehindLeftRot, BehindRightPWM, BehindRightRot);
      udp.beginPacket(udp.remoteIP(), udp.remotePort());
      udp.write((const uint8_t *)"Controlled", strlen("Controlled"));
      udp.endPacket();
      delay(50);
    }
  } else if (command.startsWith("BUZZER")) {
    BuzzerSong();
    udp.beginPacket(udp.remoteIP(), udp.remotePort());
    udp.write((const uint8_t *)"Buzzer Ring On", strlen("Buzzer Ring On"));
    udp.endPacket();
  }
  stopEngines();
}





// Motorları durdurma fonksiyonu
void stopEngines() {
  analogWrite(Front_Left_PWM, 0);
  analogWrite(Front_Right_PWM, 0);
  analogWrite(Behind_Left_PWM, 0);
  analogWrite(Behind_Right_PWM, 0);

}


// Motor kontrol fonksiyonu
void controll(int FrontLeft, int FrontLeftRotation, int FrontRight, int FrontRightRotation, int BehindLeft, int BehindLeftRotation, int BehindRight, int BehindRightRotation) {
  //front
  if (FrontLeftRotation) {
    analogWrite(Front_Left_PWM, FrontLeft);
    digitalWrite(Front_Left_in1, HIGH);
    digitalWrite(Front_Left_in2, LOW);
  } else {
    analogWrite(Front_Left_PWM, FrontLeft);
    digitalWrite(Front_Left_in1, LOW);
    digitalWrite(Front_Left_in2, HIGH);
  }

  if (FrontRightRotation) {
    analogWrite(Front_Right_PWM, FrontRight);
    digitalWrite(Front_Right_in3, HIGH);
    digitalWrite(Front_Right_in4, LOW);
  } else {
    analogWrite(Front_Right_PWM, FrontRight);
    digitalWrite(Front_Right_in3, LOW);
    digitalWrite(Front_Right_in4, HIGH);
  }

  //behind
  if (BehindLeftRotation) {
    analogWrite(Behind_Left_PWM, BehindLeft);
    digitalWrite(Behind_Left_in1, HIGH);
    digitalWrite(Behind_Left_in2, LOW);
  } else {
    analogWrite(Behind_Left_PWM, BehindLeft);
    digitalWrite(Behind_Left_in1, LOW);
    digitalWrite(Behind_Left_in2, HIGH);
  }

  if (BehindRightRotation) {
    analogWrite(Behind_Right_PWM, BehindRight);
    digitalWrite(Behind_Right_in3, HIGH);
    digitalWrite(Behind_Right_in4, LOW);
  } else {
    analogWrite(Behind_Right_PWM, BehindRight);
    digitalWrite(Behind_Right_in3, LOW);
    digitalWrite(Behind_Right_in4, HIGH);
  }
}

// Buzzer melodisi
void BuzzerSong() {
  for (int thisNote = 0; thisNote < 8; thisNote++) {
    int noteDuration = 1000 / noteDurations[thisNote];
    tone(buzzerPin, melody[thisNote], noteDuration);
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    noTone(buzzerPin);
  }
}
