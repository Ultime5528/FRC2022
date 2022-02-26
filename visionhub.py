import numpy as np
import cv2
from networktables import NetworkTables
from cscore import CameraServer


class Target:
    def __init__(self, y):
        self.y = y
        self.positions = []
        self.error = 0

    @property
    def score(self):
        return len(self.positions)


def main():
    NetworkTables.initialize(server="127.0.0.1")
    nt_normx = NetworkTables.getEntry("Vision/Hub/Norm_X")
    nt_normy = NetworkTables.getEntry("Vision/Hub/Norm_Y")

    CameraServer.kBasePort = 1183
    cs = CameraServer.getInstance()
    cs.enableLogging()

    camera = cs.startAutomaticCapture(dev=0)
    camera.setResolution(320, 240)
    camera.setFPS(30)
    camera.setBrightness(0)
    camera.setExposureManual(0)
    camera.setWhiteBalanceManual(6000)

    cvSink = cs.getVideo()

    outputStream = cs.putVideo("Hub", 320, 240)

    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)


    lowerGreen = (50, 0, 160)
    highGreen = (100, 255, 255)


    while True:
        ret, img = cvSink.grabFrame(img)
        if ret == 0:
            outputStream.notifyError(cvSink.getError())
            continue

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lowerGreen, highGreen)
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imshow('mask', mask)

        validRects = []
        if cnts is not None:
            for cnt in cnts:
                area = cv2.contourArea(cnt)
                minRect = cv2.minAreaRect(cnt)
                (_, _), (minW, minH), angle = minRect

                minRect = np.int0(cv2.boxPoints(minRect))
                minArea = cv2.contourArea(minRect)
                rectangularity = area / minArea if minArea else 0
                if rectangularity >= 0.75:
                    x, y, w, h = cv2.boundingRect(cnt)
                    if 1.25 <= minW / minH <= 3.5 and minH >= 10 and minW >= 10:
                        validRects.append((x, y, w, h))
        validPositions = []

        for x, y, w, h in validRects:
            xCenter = x + (w / 2)
            yCenter = y + (h / 2)
            validPositions.append((xCenter, yCenter))

        maxErrorX = int(img.shape[1] * 0.4)
        maxErrorY = int(img.shape[0] * 0.20)
        targets = []

        for targetX, targetY in validPositions:
            target = Target(targetY)
            for x, y in validPositions:
                if abs(targetY - y) < maxErrorY and abs(targetX - x) < maxErrorX:
                    target.positions.append((x, y))
                    target.error += abs(targetY - y)
            targets.append(target)

        if targets:
            bestTarget = targets[0]

            for target in targets[1:]:
                if bestTarget.score == target.score:
                    if target.error <= bestTarget.error:
                        bestTarget = target
                elif bestTarget.score <= target.score:
                    bestTarget = target


            position = np.mean(bestTarget.positions, axis=0).astype("int")
            norm_x = (position[0] / img.shape[1]) * 2 - 1
            norm_y = (position[1] / img.shape[0]) * 2 - 1
            nt_normx.setDouble(norm_x)
            nt_normy.setDouble(norm_y)


            cv2.circle(img, position, 3, (255, 0 ,255), 3)
        outputStream.putFrame(img)

if __name__ == '__main__':
    main()