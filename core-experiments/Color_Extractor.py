import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# stackImages(<scale>, [<horizontal images>], [<the horizontoal images below>])

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def save_image(result):
    if result is None:
        messagebox.showwarning("Warning", "No image to save")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
    if file_path:
        cv2.imwrite(file_path, result)

    else:
        messagebox.showinfo("Info", "Save operation cancelled")


original = None
result = None

window = tk.Tk()
window.withdraw()

file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])

if file_path is not None:
    original = cv2.imread(file_path)  

else:
    messagebox.showinfo("Info", "No file selected")


if original is None:
    messagebox.showerror("Error", "Image not found")
    exit()

messagebox.showinfo("Info", "Press 's' to save the result image, or 'q' to quit without saving.")

length = original.shape[1]
width = original.shape[0]

if length > width:
    original = cv2.resize(original, (850, int(850 * width / length)))
else:
    original = cv2.resize(original, (int(700 * length / width), 700))

hsv = cv2.cvtColor(original, cv2.COLOR_BGR2HSV)

cv2.namedWindow('Trackbars')
cv2.resizeWindow('Trackbars', 640, 240)

cv2.createTrackbar('Hue Min', 'Trackbars', 0, 179, lambda x: None)
cv2.createTrackbar('Hue Max', 'Trackbars', 179, 179, lambda x: None)
cv2.createTrackbar('Sat Min', 'Trackbars', 0, 255, lambda x: None)
cv2.createTrackbar('Sat Max', 'Trackbars', 255, 255, lambda x: None)
cv2.createTrackbar('Val Min', 'Trackbars', 0, 255, lambda x: None)
cv2.createTrackbar('Val Max', 'Trackbars', 255, 255, lambda x: None)

while True:

    h_min = cv2.getTrackbarPos('Hue Min', 'Trackbars')
    h_max = cv2.getTrackbarPos('Hue Max', 'Trackbars')
    s_min = cv2.getTrackbarPos('Sat Min', 'Trackbars')
    s_max = cv2.getTrackbarPos('Sat Max', 'Trackbars')
    v_min = cv2.getTrackbarPos('Val Min', 'Trackbars')
    v_max = cv2.getTrackbarPos('Val Max', 'Trackbars')

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(hsv, lower, upper)

    result = cv2.bitwise_and(original, original, mask=mask)

    #cv2.imshow('original', original)
    #cv2.imshow('Mask', mask)
    #cv2.imshow('Result', result)
    Final = stackImages(0.6, ([original, mask], [hsv, result]))
    cv2.imshow('Color Extractor', Final)


    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('s'):
        save_image(result)
        print("h_min:", h_min)
        print("h_max:", h_max)
        print("s_min:", s_min)
        print("s_max:", s_max)
        print("v_min:", v_min)
        print("v_max:", v_max)
        break

cv2.destroyAllWindows()

window.destroy()
