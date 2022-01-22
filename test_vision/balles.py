import numpy as np
import cv2



def Balles(img, color, error, param2, minRad, maxRad):
    centreX = 0
    centreY = 0

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if color == "rouge":
        mask1 = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
        mask2 = cv2.inRange(hsv, (170, 100, 100), (180, 255, 255))
        mask = cv2.bitwise_or(mask1, mask2)

    if color == "bleu":
        mask = cv2.inRange(hsv, (90, 100, 50), (130, 255, 255))

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur = cv2.bilateralFilter(gray, 9 ,75, 75)
    blur = cv2.medianBlur(gray, 5)
    # blur = cv2.blur(gray, (5, 5))
    # blur = cv2.GaussianBlur(gray, (17, 17), 0)
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1.5, 100, param1=100, param2=param2, minRadius=minRad, maxRadius=maxRad)

    infoCercles = []
    if circles is not None:
        centres = []
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            if w >= 10 and h >= 10:
                centreX = x + (w / 2)
                centreY = y + (h / 2) - 20
                centres.append((centreX, centreY))

        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:
            for centreX, centreY in centres:
                cv2.circle(img, (i[0], i[1]), 3, (255, 255, 255, 5))
                if centreX >= i[0] - i[2] + error and centreX <= i[0] + i[2] - error and centreY >= i[1] - i[2] + error and centreY <= i[1] + i[2] - error:
                    cercleX = i[0] - i[2]
                    cercleY = i[1] + i[2]
                    cercleWH = i[2] * 2
                    infoCercles.append((cercleX, cercleY, cercleWH))
                    break
    cv2.imshow("mask", mask)
    cv2.imshow("blur", blur)
    cv2.imshow("gray", gray)
    return infoCercles

