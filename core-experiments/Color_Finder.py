import cv2
import numpy as np

lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])

lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])

lower_green = np.array([40, 50, 50])
upper_green = np.array([80, 255, 255])

lower_yellow = np.array([20, 50, 50])
upper_yellow = np.array([30, 255, 255])

lower_orange = np.array([10, 50, 50])
upper_orange = np.array([20, 255, 255])

lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 30, 255])

cam = cv2.VideoCapture(0)

def selector(image_list):
    options = ['White', 'Red', 'Blue', 'Orange', 'Green', 'Yellow']
    dom = 0
    dom_index = -1
    
    
    for i in range(len(image_list)): 
        col = cv2.countNonZero(image_list[i])
        if col > dom:
            dom = col
            dom_index = i
            
    if dom <= 500 or dom_index == -1:
        return "No Color Detected"
    else:
        return options[dom_index]


while True:

    ret, frame = cam.read()

    if not ret:
        print("Camera access error")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

    masks = [mask_white, mask_red, mask_blue, mask_orange, mask_green, mask_yellow]

    #print("Detected Color:", selector(masks))

    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = cv2.rectangle(frame, (0, frame.shape[0] - 30), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
    frame = cv2.putText(frame, "Detected Color: " + selector(masks), (10, frame.shape[0] - 10), font, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('Color Detection', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()