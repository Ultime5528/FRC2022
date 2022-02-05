import numpy as np
import cv2


class Target:
    def __init__(self, y):
        self.y = y
        self.positions = []
        self.error = 0

    @property
    def score(self):
        return len(self.positions)


def hub(img):
    lowerGreen = (50, 100, 160)
    highGreen = (100, 255, 255)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerGreen, highGreen)
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('mask', mask)

    validRects = []
    if cnts is not None:
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            minRect = cv2.minAreaRect(cnt)
            minRect = np.int0(cv2.boxPoints(minRect))
            minArea = cv2.contourArea(minRect)
            rectangularity = area / minArea if minArea else 0
            if rectangularity >= 0.6:
                x, y, w, h = cv2.boundingRect(cnt)
                if 1.25 <= w / h <= 3.5 and w >= 10 and h >= 10:
                    validRects.append((x, y, w, h))
    validPositions = []

    for x, y, w, h in validRects:
        xCenter = x + (w / 2)
        yCenter = y + (h / 2)
        validPositions.append((xCenter, yCenter))

    errorX = int(img.shape[1] / 10)
    errorY = int(img.shape[0] / 10)
    targets = []

    for targetX, targetY in validPositions:
        target = Target(targetY)
        for x, y in validPositions:
            if abs(targetY - y) < errorY and abs(targetX - x) < errorX:
                target.positions.append((x, y))
                target.error += abs(targetY - y)
        targets.append(target)

    bestTarget = targets[0]

    for target in targets[1:]:
        if bestTarget.score == target.score:
            if target.error <= bestTarget.error:
                bestTarget = target
        elif bestTarget.score <= target.score:
            bestTarget = target

    position = np.mean(bestTarget.positions, axis=0).astype("int")

    return position