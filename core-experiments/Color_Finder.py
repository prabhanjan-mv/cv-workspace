import cv2
import numpy as np

lower_blue = np.array([90, 60, 60])
upper_blue = np.array([130, 255, 255])

lower_red1 = np.array([0, 70, 60])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 70, 60])
upper_red2 = np.array([180, 255, 255])

lower_green = np.array([36, 60, 60])
upper_green = np.array([89, 255, 255])

lower_yellow = np.array([26, 70, 60])
upper_yellow = np.array([35, 255, 255])

lower_orange = np.array([11, 80, 60])
upper_orange = np.array([25, 255, 255])

lower_white = np.array([0, 0, 180])
upper_white = np.array([180, 40, 255])

lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 45, 45])

cam = cv2.VideoCapture(0)

def selector(image_list):               # Returns the Dominant Color
    options = ['White', 'Red', 'Blue', 'Orange', 'Green', 'Yellow', "Black"]
    dom = 0
    dom_index = -1

    # Checks which color's mask in the image list has the highest number of true pixles
    
    for i in range(len(image_list)): 
        col = cv2.countNonZero(image_list[i])
        if col > dom:
            dom = col
            dom_index = i
            
    if dom <= 10000 or dom_index == -1:
        return "No Color Detected"
    else:
        return options[dom_index]


while True:

    ret, frame = cam.read()

    if not ret:
        print("Camera access error")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # All Masks

    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_black = cv2.inRange(hsv, lower_black, upper_black)

    masks = [mask_white, mask_red, mask_blue, mask_orange, mask_green, mask_yellow, mask_black]

    # Putting Up Text On Screen

    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = cv2.rectangle(frame, (0, frame.shape[0] - 30), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
    frame = cv2.putText(frame, "Detected Color: " + selector(masks), (10, frame.shape[0] - 10), font, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('Color Detection', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
