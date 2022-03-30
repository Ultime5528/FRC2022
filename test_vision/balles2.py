import math

import cv2


def Balles2(img, color, error):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if color == "rouge":
        mask1 = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
        mask2 = cv2.inRange(hsv, (170, 100, 100), (180, 255, 255))
        mask = cv2.bitwise_or(mask1, mask2)

    if color == "bleu":
        mask = cv2.inRange(hsv, (90, 86, 50), (130, 255, 255))

    blur = cv2.medianBlur(mask, 5)
    cnts, _ = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    infoCercles = []

    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        if w and h >= 20:
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            # cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
            circularity = 4 * math.pi * area / perimeter ** 2 if perimeter else 0
            if abs(1 - circularity) <= error:
                # cv2.drawContours(img, [cnt], -1, (255, 0, 0), 3)
                cercleX = round(x)
                cercleY = round(y)
                cercleW = round(w)
                cercleH = round(h)

                infoCercles.append((cercleX, cercleY, cercleW, cercleH))
    cv2.imshow("mask", blur)
    return infoCercles
