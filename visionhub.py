import threading

import numpy as np
import cv2
from networktables import NetworkTables
from cscore import CameraServer

isConnected = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    with isConnected:
        notified[0] = True
        isConnected.notify()
    print("NetworkTables connected :", connected)
    print(info)

class Target:
    def __init__(self, y):
        self.y = y
        self.positions = []
        self.error = 0

    @property
    def score(self):
        return len(self.positions)


def hub_loop():
    NetworkTables.initialize(server="10.55.28.2")
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
    # with isConnected:
    #     print("Waiting for connection...")
    #     if not notified[0]:
    #         isConnected.wait()
    # print("Connected!")

    nt_normx = NetworkTables.getEntry("/Vision/Hub/Norm_X")
    nt_normy = NetworkTables.getEntry("/Vision/Hub/Norm_Y")
    nt_found = NetworkTables.getEntry("/Vision/Hub/Found")
    nt_found.setBoolean(False)

    cs = CameraServer.getInstance()
    cs.kBasePort = 1181
    cs.enableLogging()

    hub_cam = cs.startAutomaticCapture(name="hub_cam", path="/dev/v4l/by-id/usb-Microsoft_Microsoft®_LifeCam_HD-3000-video-index0")
    hub_cam.setResolution(320, 240)
    hub_cam.setFPS(30)
    hub_cam.setBrightness(0)
    hub_cam.setExposureManual(0)
    hub_cam.setWhiteBalanceManual(6000)

    cvSink = cs.getVideo(camera=hub_cam)

    outputStream = cs.putVideo("Hub", 320, 240)
    binStream = cs.putVideo("Hub bin", 320, 240)

    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)


    lowerGreen = (50, 0, 160)
    highGreen = (100, 255, 200)


    while True:
        ret, img = cvSink.grabFrame(img)
        if ret == 0:
            outputStream.notifyError(cvSink.getError())
            continue

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lowerGreen, highGreen)
        _, cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imshow('mask', mask)
        img_cnts = cv2.drawContours(img.copy(), cnts, -1, (0, 0, 255), -1)

        validRects = []
        if cnts is not None:
            print("==========")
            print("nb cnts :", len(cnts))
            for cnt in cnts:
                print("---")
                area = cv2.contourArea(cnt)
                print("area", area)
                perimeter = cv2.arcLength(cnt, True)
                print("perimeter :", perimeter)
                minRect = cv2.minAreaRect(cnt)
                (_, _), (minW, minH), _ = minRect
                print("minW :", minW)
                print("minH :", minH)

                minRect = np.int0(cv2.boxPoints(minRect))
                minArea = cv2.contourArea(minRect)
                print("minArea :", minArea)

                rectangularity = area / minArea if minArea else 0
                print("rectangularity :", rectangularity)

                if rectangularity >= 0.5 and perimeter >= 7:
                    x, y, w, h = cv2.boundingRect(cnt)
                    ratio = max(w, h) / min(w, h)
                    print("rapport :", ratio)
                    if 1.25 <= ratio <= 3.5 and w > h:
                        validRects.append((x, y, w, h))

        for (x, y, w, h) in validRects:
            cv2.rectangle(img_cnts, (x, y), (x + w, y + h), (0, 255, 255), 1)

        binStream.putFrame(img_cnts)
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
            nt_found.setBoolean(True)

            NetworkTables.flush()

            cv2.circle(img, tuple(position), 3, (255, 0 ,255), 3)
        else:
            nt_found.setBoolean(False)

        outputStream.putFrame(img)
        yield


def main():
    loop = hub_loop()
    while True:
        next(loop)


if __name__ == '__main__':
    main()
