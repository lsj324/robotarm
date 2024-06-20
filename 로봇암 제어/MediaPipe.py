# 관절들의 각도에 따라 로봇팔 제어

import mediapipe as mp
import cv2
import numpy as np
import sys
import serial
import time

count = 0

ser = serial.Serial('COM5', 9600)
time.sleep(2)

# 시리얼 통신
def send_angles(base_angle_serial, shoulder_angle_serial, arm_angle_serial, head_angle_serial):
    base_angle = base_angle_serial
    shoulder_angle = shoulder_angle_serial
    arm_angle = arm_angle_serial
    head_angle = head_angle_serial

    print(base_angle_serial, shoulder_angle_serial, arm_angle_serial, head_angle_serial)
    # 값 보내기
    ser.write("{:d} {:d} {:d} {:d}\n".format(base_angle, shoulder_angle, arm_angle, head_angle).encode())

def calculate_angle(s, e, h):
    a = np.array(s)  # First
    b = np.array(e)  # Mid
    c = np.array(h)  # End
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1020)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

if not cap.isOpened():
    print("Could not open camera")
    sys.exit()

pos = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

while True:
    ret, frame = cap.read()
    count += 1
    print(count)

    if not ret:
        print("can't load background")
        sys.exit()
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pos.process(frame_rgb)
    try:
        #  Mediapipe로 관절에 관한 좌표 정보 얻기
        landmarks = results.pose_landmarks.landmark


        # 각 관절 좌표 정보 얻기
        elbow = landmarks[13]

        x_e = int(elbow.x * frame.shape[1])
        y_e = int(elbow.y * frame.shape[0])

        hand = landmarks[15]

        x_h = int(hand.x * frame.shape[1])
        y_h = int(hand.y * frame.shape[0])

        shoulder = landmarks[11]

        x_s = int(shoulder.x * frame.shape[1])
        y_s = int(shoulder.y * frame.shape[0])
        # mp_drawing.draw_landmarks(frame, landmarks, mp_pose.POSE_CONNECTIONS,mp_drawing.DrawingSpec((255,0,0),2,2))

        # 관절에 점 찍기
        cv2.circle(frame, (x_e, y_e), radius=5, color=(0, 0, 255), thickness=-1)
        cv2.circle(frame, (x_h, y_h), radius=5, color=(0, 0, 255), thickness=-1)
        cv2.circle(frame, (x_s, y_s), radius=5, color=(0, 0, 255), thickness=-1)
        # 각 점 사이 선으로 잇기
        cv2.line(frame, (x_e, y_e), (x_h, y_h), color=(0, 0, 255))
        cv2.line(frame, (x_e, y_e), (x_s, y_s), color=(0, 0, 255))
        
        # 각 관절 좌표 x,y
        s = [shoulder.x, shoulder.y]
        e = [elbow.x, elbow.y]
        h = [hand.x, hand.y]

        # 각도 계산
        angle = calculate_angle(s, e, h)

        # 아두이노에 통신 보내기
        # 해당 루프가 반복될 때마다 count 값이 1씩 증가하고
        # 5가 될 시 각도값을 로봇팔 아두이노에 전달
        if count == 5:
            send_angles(90, 90, angle.astype(int), 90)
            count = 0
    except:
        pass
    # 영상 좌우 반전
    frame_flip = cv2.flip(frame, 1)

    cv2.imshow('MediaPipe', frame_flip)

cap.release()
cv2.destroyAllWindows()