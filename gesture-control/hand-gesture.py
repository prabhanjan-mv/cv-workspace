import time
import cv2
import mediapipe as mp
import pyautogui

from HandConnections import HandConnections

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode
mp_Draw = mp.tasks.vision.drawing_utils

pyautogui.FAILSAFE = False

# ------- GESTURE DATA ------#

class Gesture:
    def __init__(self, name, distances):
        self.name = name
        self.distances = distances

thumbsUp = Gesture('ThumbsUp', [1.65348, 0.93389, 0.83877, 0.75221, 0.71309, 1.26117, 0.23806, 0.22914, 0.22526, 1.85236])
rock = Gesture('Rock', [0.74459, 1.985, 0.72132, 0.67404, 1.76736, 1.28045, 1.34241, 0.15406, 1.13853, 1.10872])
call = Gesture('Call', [1.49028, 0.92797, 0.73658, 0.64209, 1.59166, 0.8891, 0.22422, 0.17217, 1.01162, 1.76389])
ninja = Gesture('Ninja', [0.73878, 1.85103, 1.93531, 0.58069, 0.49539, 1.13916, 0.1499, 1.41506, 0.1233, 0.34207])
pointer = Gesture('Pointer', [1.28966, 2.15179, 0.64928, 0.49891, 0.52367, 1.60805, 1.66635, 0.20087, 0.14328, 1.22042])
click = Gesture('Click', [1.3128, 2.17557, 0.62589, 0.44943, 0.49774, 0.99521, 1.73894, 0.22429, 0.15258, 1.04185])
thumbsLeft = Gesture('ThumbsLeft', [1.17525, 0.50848, 0.3922, 0.37145, 0.4938, 0.78409, 0.14816, 0.15364, 0.17794, 1.13129])
thumbsRight = Gesture('ThumbsRight', [1.07955, 0.70998, 0.68557, 0.66561, 0.65867, 0.67034, 0.13439, 0.13682, 0.15803, 1.0882])

saved_gestures = [thumbsUp, rock, call, ninja, pointer, click, thumbsLeft, thumbsRight]

current_gesture = None

last_gesture = None

#-----------------------------#




# ----- GESTURE PROCESSING ----- #

def dist(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2) ** 0.5


def gesture_locator(thumb, index, middle, ring, pinky, wrist, anchor):

    #name = input("Enter the name of the gesture: ")
    thumb_ = (thumb.x, thumb.y, thumb.z)
    index_ = (index.x, index.y, index.z)
    middle_ = (middle.x, middle.y, middle.z)
    ring_ = (ring.x, ring.y, ring.z)
    pinky_ = (pinky.x, pinky.y, pinky.z)
    wrist_ = (wrist.x, wrist.y, wrist.z)
    anchor_ = (anchor.x, anchor.y, anchor.z)

    normal = dist(wrist_, anchor_)

    #FORMAT - Wrist to Thumb, Index, Middle, Ring, Pinky, Thumb_Index, Index_Middle, Middle_Ring, Ring_Pinky, Pinky_Thumb
    distances = [dist(wrist_, thumb_), dist(wrist_, index_), dist(wrist_, middle_), dist(wrist_, ring_), dist(wrist_, pinky_), dist(thumb_, index_), dist(index_, middle_), dist(middle_, ring_), dist(ring_, pinky_), dist(pinky_, thumb_)]
    normal_distance = []

    for i in distances:
        normal_distance.append(round(i/normal, 5))

    return normal_distance

def gesture_detector(thumb, index, middle, ring, pinky, wrist, anchor):

    current_distance = gesture_locator(thumb, index, middle, ring, pinky, wrist, anchor)

    best_match = "Unknown"
    lowest_error = 0.1  #error threshold

    for gesture in saved_gestures:
        
        error = sum(abs(c - s) for c, s in zip(current_distance, gesture.distances)) / len(current_distance)
        
        if error < lowest_error:
            lowest_error = error
            best_match = gesture.name

    global current_gesture
    current_gesture = best_match

#-----------------------------#

# ------ GESTURE BASED TASKS ----- #

prev_x = None
prev_y = None
smooth_move_x = 0
smooth_move_y = 0

def Pointer(index):

    global prev_x, prev_y, smooth_move_x, smooth_move_y

    current_x = index.x
    current_y = index.y

    if prev_x is None or prev_y is None:
        prev_x = current_x
        prev_y = current_y
        return

    delta_x = current_x - prev_x
    delta_y = current_y - prev_y

    sensitivity = 7500
    smoothing = 0.3

    raw_move_x = int(delta_x * sensitivity)
    raw_move_y = int(delta_y * sensitivity)

    smooth_move_x = int((raw_move_x * smoothing) + (smooth_move_x * (1 - smoothing)))
    smooth_move_y = int((raw_move_y * smoothing) + (smooth_move_y * (1 - smoothing)))

    pyautogui.moveRel(smooth_move_x, smooth_move_y)

    prev_x = current_x
    prev_y = current_y



#-----------------------------#


# ----- LIVE FOOTAGE PROCCESING ----- #

latest_result = None

def receive_prediction_callback(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
    global latest_result
    latest_result = result

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"), 
    running_mode=VisionRunningMode.LIVE_STREAM,                       
    num_hands=1,
    result_callback=receive_prediction_callback
    )

with HandLandmarker.create_from_options(options) as landmarker:

    while cap.isOpened():

        success, img = cap.read()

        img = cv2.flip(img, 1)

        h, w, c = img.shape

        if not success:
            break

        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data= rgb_img)

        frame_timestamp_ms = int(time.time() * 1000)
        landmarker.detect_async(mp_image, frame_timestamp_ms)

        if latest_result and latest_result.hand_landmarks:
            for idx, hand_landmarks in enumerate(latest_result.hand_landmarks):

                thumb = hand_landmarks[4]
                index = hand_landmarks[8]
                middle = hand_landmarks[12]
                ring = hand_landmarks[16]
                pinky = hand_landmarks[20]
                wrist = hand_landmarks[0]
                anchor = hand_landmarks[9]

                HandConnections(img, hand_landmarks, (0,0,0))

                cv2.circle(img, (int(thumb.x * w), int(thumb.y * h)), 5, (0, 255, 0), -1)
                cv2.circle(img, (int(index.x * w), int(index.y * h)), 5, (0, 255, 0), -1)
                cv2.circle(img, (int(middle.x * w), int(middle.y * h)), 5, (0, 255, 0), -1)
                cv2.circle(img, (int(ring.x * w), int(ring.y * h)), 5, (0, 255, 0), -1)
                cv2.circle(img, (int(pinky.x * w), int(pinky.y * h)), 5, (0, 255, 0), -1)
                cv2.circle(img, (int(wrist.x * w), int(wrist.y * h)), 5, (0, 255, 0), -1)
                #cv2.circle(img, (int(anchor.x * w), int(anchor.y * h)), 5, (0, 255, 0), -1)

                gesture_detector(thumb, index, middle, ring, pinky, wrist, anchor)


                if current_gesture == "Pointer":
                    try:
                        Pointer(index)
                        last_gesture = current_gesture

                    except (pyautogui.FailSafeException, KeyboardInterrupt):
                        width, height = pyautogui.size()
                        pyautogui.moveTo(width / 2, height / 2)

                elif current_gesture == "Click" and not last_gesture == "Click":
                    pyautogui.leftClick()

                    last_gesture = current_gesture
                    prev_x = None
                    prev_y = None

                elif current_gesture == "Rock" and not last_gesture == "Rock":

                    pyautogui.hotkey('win')

                    last_gesture = current_gesture

                elif current_gesture == "thumbsLeft" and not last_gesture == "thumbsLeft":

                    pyautogui.hotkey('ctrl', 'shift', 'esc')

                    last_gesture = current_gesture

                elif current_gesture == "thumbsRight" and not last_gesture == "thumbsRight":

                    pyautogui.hotkey('ctrl', 'win', 'right')

                    last_gesture = current_gesture


                cv2.putText(img, current_gesture, (0, h - 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 5, cv2.LINE_AA)
                cv2.putText(img, last_gesture, (0, h - 60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 5, cv2.LINE_AA)


        cv2.imshow("Image", img)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

        if key == ord('s'):
            print(gesture_locator(thumb, index, middle, ring, pinky, wrist, anchor))


cap.release()
cv2.destroyAllWindows()
