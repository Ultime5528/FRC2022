
import numpy as np
import cv2

img = cv2.imread(r'C:\Users\plega\OneDrive\Bureau\New folder (2)\TarmacCenter3ft10in.png')


def but(img):
    lowerGreen = (50, 50, 50)
    highGreen = (100, 255, 255)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerGreen, highGreen)
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    validRects = []
    if cnts is not None:
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            minRect = cv2.minAreaRect(cnt)
            minRect = np.int0(cv2.boxPoints(minRect))
            minArea = cv2.contourArea(minRect)
            rectangularity = area / minArea if minArea else 0
            if rectangularity >= 0.75:
                x, y, w, h = cv2.boundingRect(cnt)
                if 1.25 <= w / h <= 3.5 and w >= 10 and h >= 10:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
                    validRects.append((x, y, w, h))

    validXs = []
    validYs = []
    for x, y, w, h in validRects:
        xCenter = x + (w / 2)
        validXs.append(xCenter)
        yCenter = y + (h / 2)
        validYs.append(yCenter)

    validX = int(sum(validXs) / len(validXs))
    validY = int(sum(validYs) / len(validYs))

    return validX, validY


validX, validY = but(img)
cv2.circle(img, (validX, validY), 3, (255, 255, 0), 3)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
