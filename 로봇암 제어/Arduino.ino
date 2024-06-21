#include <Servo.h>

Servo base_servo;
Servo shoulder_servo;
Servo elbow_servo;
Servo wrist_servo;

void setup() {
  Serial.begin(9600); // 시리얼 통신을 9600bps로 시작

  // 서보 모터 초기화
  base_servo.attach(9);     // 베이스 서보 핀 (9번 핀에 연결)
  shoulder_servo.attach(10); // 숄더 서보 핀 (10번 핀에 연결)
  elbow_servo.attach(11);    // 엘보 서보 핀 (11번 핀에 연결)
  wrist_servo.attach(12);    // 손목 서보 핀 (12번 핀에 연결)
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int first_index = data.indexOf(' ');
    int second_index = data.indexOf(' ', first_index + 1);
    int third_index = data.indexOf(' ', second_index + 1);

    int base_ang = data.substring(0, first_index).toInt();
    int shoulder_ang = data.substring(first_index + 1, second_space).toInt();
    int elbow_ang = data.substring(second_index + 1, third_space).toInt();
    int wrist_ang = data.substring(third_index + 1).toInt();

    // 서보 모터 각도 설정
    base_servo.write(base_ang);
    shoulder_servo.write(shoulder_ang);
    elbow_servo.write(elbow_ang);
    wrist_servo.write(wrist_ang);
  }
}
