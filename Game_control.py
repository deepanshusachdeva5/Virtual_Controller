import cv2
import numpy as np
from pynput.keyboard import Key, Controller


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

myColors = [[71, 74, 33, 105, 255, 255]]

myColorValues = [[204, 204, 0]]

myPoints = []


def findColor(img, myColors, myColorValues):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    count = 0
    newPoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])

        mask = cv2.inRange(img_hsv, lower, upper)
        x, y = getContours(mask)

        cv2.circle(copy_frame, (x, y), 5, myColorValues[count], cv2.FILLED)

        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
    return x, y


def getContours(img):
    x, y, w, h = 0, 0, 0, 0
    contours, heirarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 80:
            cv2.drawContours(copy_frame, cnt, -1, (255, 0, 255), 3)
            peri = cv2.arcLength(cnt, True)

            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)

            x, y, w, h = cv2.boundingRect(approx)

    return x+w//2, y


keyboard = Controller()
centre = [320, 240]

while True:

    success, frame = cap.read()

    frame = cv2.flip(frame, 1)
    copy_frame = frame.copy()

    # preprocessing(frame_hsv)
    pos_x, pos_y = findColor(frame, myColors, myColorValues)
    if pos_x != 0 and pos_y != 0:
        if pos_x < centre[0]-20:
            print("right pressed")
            keyboard.press(Key.left)
            keyboard.release(Key.left)
        elif pos_x > centre[0]+20:
            print("left_pressed")
            keyboard.press(Key.right)
            keyboard.release(Key.right)
        if pos_y < centre[1]-20:
            print("up")
            keyboard.press(Key.up)
            keyboard.release(Key.up)
        elif pos_y > centre[1]+20:
            print("down")
            keyboard.press(Key.down)
            keyboard.release(Key.down)
        centre[0] = pos_x
        centre[1] = pos_y

    cv2.circle(copy_frame, (centre[0], centre[1]), 40, (255, 0, 0), 2)
    cv2.imshow("frame", copy_frame)
    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
