import numpy as np
import cv2

img = cv2.imread('C:/Users/filal/Desktop/Frc2022/Balls/DSC01667.jpg')
centreX = 0
centreY = 0

def red():
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, (0, 100, 100), (15, 255, 255))
    mask2 = cv2.inRange(hsv, (165, 100, 100), (180, 255, 255))
    mask = cv2.bitwise_or(mask1, mask2)
    blur = cv2.medianBlur(mask, 5)
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.5, 100, param1=30, param2=20, minRadius=30, maxRadius=100)
    cnts, _ = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow('red', blur)
    cv2.waitKey(0)

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
                    cv2.circle(img, (i[0], i[1]), i[2], (0, 0, 255), 3)
                    cv2.circle(img, (i[0], i[1]), 3, (255, 255, 255), 3)
                    break



def blue():
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (90, 100, 0), (130, 255, 255))
    blur = cv2.medianBlur(mask, 5)
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.2, 100, param1=30, param2=25, minRadius=30, maxRadius=400)
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow('blue', blur)
    cv2.waitKey(0)

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
                    cv2.circle(img, (i[0], i[1]), i[2], (0, 0, 255), 3)
                    cv2.circle(img, (i[0], i[1]), 3, (255, 255, 255), 3)
                    break

# red()
blue()
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# if circles is not None:
#     circles = np.uint16(np.around(circles))
#     for i in circles[0, :]:
#         cv2.circle(img, (i[0], i[1]), i[2], (255, 0, 0), 3)
#         cv2.circle(img, (i[0], i[1]), 3, (255, 255, 255), 3)