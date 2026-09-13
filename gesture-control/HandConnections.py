import cv2
import mediapipe as mp

def HandConnections(img, hand_landmarks, color = (255,0,0)):

    h, w, _ = img.shape

    for i in range(0, 4):
        cv2.line(img, (int(hand_landmarks[i].x * w), int(hand_landmarks[i].y * h)), (int(hand_landmarks[i+1].x * w), int(hand_landmarks[i+1].y * h)), color, thickness=2)

    for i in range(5, 8):
            cv2.line(img, (int(hand_landmarks[i].x * w), int(hand_landmarks[i].y * h)), (int(hand_landmarks[i+1].x * w), int(hand_landmarks[i+1].y * h)), color, thickness=2)

    for i in range(9, 12):
            cv2.line(img, (int(hand_landmarks[i].x * w), int(hand_landmarks[i].y * h)), (int(hand_landmarks[i+1].x * w), int(hand_landmarks[i+1].y * h)), color, thickness=2)

    for i in range(13, 16):
            cv2.line(img, (int(hand_landmarks[i].x * w), int(hand_landmarks[i].y * h)), (int(hand_landmarks[i+1].x * w), int(hand_landmarks[i+1].y * h)), color, thickness=2)

    for i in range(17, 20):
            cv2.line(img, (int(hand_landmarks[i].x * w), int(hand_landmarks[i].y * h)), (int(hand_landmarks[i+1].x * w), int(hand_landmarks[i+1].y * h)), color, thickness=2)    


    cv2.line(img, (int(hand_landmarks[2].x * w), int(hand_landmarks[2].y * h)), (int(hand_landmarks[5].x * w), int(hand_landmarks[5].y * h)), color, thickness=2)
    cv2.line(img, (int(hand_landmarks[5].x * w), int(hand_landmarks[5].y * h)), (int(hand_landmarks[9].x * w), int(hand_landmarks[9].y * h)), color, thickness=2)
    cv2.line(img, (int(hand_landmarks[9].x * w), int(hand_landmarks[9].y * h)), (int(hand_landmarks[13].x * w), int(hand_landmarks[13].y * h)), color, thickness=2)
    cv2.line(img, (int(hand_landmarks[13].x * w), int(hand_landmarks[13].y * h)), (int(hand_landmarks[17].x * w), int(hand_landmarks[17].y * h)), color, thickness=2)
    cv2.line(img, (int(hand_landmarks[17].x * w), int(hand_landmarks[17].y * h)), (int(hand_landmarks[0].x * w), int(hand_landmarks[0].y * h)), color, thickness=2)