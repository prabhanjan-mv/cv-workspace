import cv2
import numpy as np

img = np.zeros((450, 800, 3), np.uint8)

img[:] = (255, 255, 255)

jpn = cv2.circle(img, (400, 225), 70, (0, 0, 255), -1)

#cv2.imshow('japan', jpn)

img[0:150,:] = (0,165,255)
img[300:450,:] = (0,255,0)

india = cv2.circle(img, (400, 225), 70, (255, 0, 0), -1)
india = cv2.circle(img, (400, 225), 60, (255, 255, 255), -1)

for i in range(0, 360, 15):
    x = int(400 + 60 * np.cos(np.radians(i)))
    y = int(225 + 60 * np.sin(np.radians(i)))

    india = cv2.line(india, (400, 225), (x, y), (255, 0, 0), 2)

cv2.imshow('india', india)

cv2.waitKey(0)
cv2.destroyAllWindows()