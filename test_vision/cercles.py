import numpy as np
import cv2



def balles(img, color):
    centreX = 0
    centreY = 0

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if color == "red":
        mask1 = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
        mask2 = cv2.inRange(hsv, (170, 100, 100), (180, 255, 255))
        mask = cv2.bitwise_or(mask1, mask2)
        circleColor = (0, 0, 255)


    if color == "blue":
        mask = cv2.inRange(hsv, (90, 100, 50), (130, 255, 255))
        circleColor = (255, 0 ,0)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    blur = cv2.medianBlur(mask, 5)
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.5, 100, param1=100, param2=25, minRadius=30, maxRadius=80)
    cnts, _ = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    infoCercles = []
    if circles is not None:
        centres = []
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            centreX = x + (w / 2)
            centreY = y + (h / 2)
            centres.append((centreX, centreY))

        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:
            for centreX, centreY in centres:
                if centreX >= i[0] - i[2] and centreX <= i[0] + i[2] and centreY >= i[1] - i[2] and centreY <= i[1] + i[2]:
                    cercleX = i[0] - i[2]
                    cercleY = i[1] + i[2]
                    cercleWH = i[2]
                    infoCercles.append((cercleX, cercleY, cercleWH))
                    break

    return infoCercles