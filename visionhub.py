import cv2
import numpy as np
from cscore import CameraServer
from networktables import NetworkTables

import properties

DEBUG = True


class Target:
    def __init__(self, y):
        self.y = y
        self.positions = []
        self.error = 0

    @property
    def score(self):
        return len(self.positions)


def hub_loop():
    nt_normx = NetworkTables.getEntry("/Vision/Hub/Norm_X")
    nt_normy = NetworkTables.getEntry("/Vision/Hub/Norm_Y")
    nt_found = NetworkTables.getEntry("/Vision/Hub/Found")
    nt_found.setBoolean(False)

    cs = CameraServer.getInstance()
    cs.kBasePort = 1181
    cs.enableLogging()

    hub_cam = cs.startAutomaticCapture(name="hub_cam",
                                       path="/dev/v4l/by-id/usb-Microsoft_Microsoft®_LifeCam_HD-3000-video-index0")
    hub_cam.setResolution(320, 240)
    hub_cam.setFPS(30)
    hub_cam.setBrightness(0)
    hub_cam.setExposureManual(0)
    hub_cam.setWhiteBalanceManual(6000)

    cvSink = cs.getVideo(camera=hub_cam)

    outputStream = cs.putVideo("Hub", 320, 240)

    if DEBUG:
        binStream = cs.putVideo("Hub bin", 320, 240)
    else:
        binStream = None

    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    while True:
        ret, img = cvSink.grabFrame(img)
        if ret == 0:
            outputStream.notifyError(cvSink.getError())
            continue

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, properties.values.vision_hub_lowergreen, properties.values.vision_hub_highergreen)

        dilate = 1
        kernel = np.ones((dilate * 2 + 1, dilate * 2 + 1), "uint8")
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)
        # mask = cv2.erode(mask, kernel, iterations=1)

        _, cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imshow('mask', mask)
        if DEBUG:
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            mask = cv2.drawContours(mask, cnts, -1, (0, 0, 255), 1)

        validRects = []
        if cnts is not None:
            for cnt in cnts:
                area = cv2.contourArea(cnt)
                perimeter = cv2.arcLength(cnt, True)
                minRect = cv2.minAreaRect(cnt)
                (_, _), (minW, minH), _ = minRect

                minRect = np.int0(cv2.boxPoints(minRect))
                minArea = cv2.contourArea(minRect)

                rectangularity = area / minArea if minArea else 0
                ratio = None

                if rectangularity >= properties.values.vision_hub_rectangularity_threshold and perimeter >= properties.values.vision_hub_perimeter_threshold:
                    x, y, w, h = cv2.boundingRect(cnt)
                    ratio = max(w, h) / min(w, h)
                    if 1.00 <= ratio <= 3.5 and w > h:
                        validRects.append((x, y, w, h))

                # if DEBUG:
                #     print("==========")
                #     print("nb cnts :", len(cnts))
                #     print("---")
                #     print("area", area)
                #     print("perimeter :", perimeter)
                #     print("minW :", minW)
                #     print("minH :", minH)
                #     print("minArea :", minArea)
                #     print("rectangularity :", rectangularity)
                #     print("rapport :", ratio)

        if binStream:
            for (x, y, w, h) in validRects:
                cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 255, 255), 1)
            binStream.putFrame(mask)

        validPositions = []

        for x, y, w, h in validRects:
            xCenter = x + (w / 2)
            yCenter = y + (h / 2)
            validPositions.append((xCenter, yCenter))

        maxErrorX = int(img.shape[1] * properties.values.vision_hub_maxErrorX_multiplier)
        maxErrorY = int(img.shape[0] * properties.values.vision_hub_maxErrorY_multiplier)
        targets = []

        for targetX, targetY in validPositions:
            target = Target(targetY)
            for x, y in validPositions:
                if abs(targetY - y) < maxErrorY and abs(targetX - x) < maxErrorX:
                    target.positions.append((x, y))
                    target.error += abs(targetY - y) + abs(targetX - x)
            targets.append(target)

        if targets:
            bestTarget = targets[0]

            for target in targets[1:]:
                if bestTarget.score == target.score:
                    if target.error <= bestTarget.error:
                        bestTarget = target
                elif bestTarget.score <= target.score:
                    bestTarget = target

            if DEBUG:
                # pass
                for p in bestTarget.positions:
                    cv2.circle(mask, (int(p[0]), int(p[1])), 3, (0, 0, 255), 5)

            position = np.mean(bestTarget.positions, axis=0).astype("int")
            norm_x = (position[0] / img.shape[1]) * 2 - 1
            norm_y = (position[1] / img.shape[0]) * 2 - 1

            nt_normx.setDouble(norm_x)
            nt_normy.setDouble(norm_y)
            nt_found.setBoolean(True)

            cv2.circle(img, tuple(position), 3, (255, 0, 255), 5)
        else:
            nt_found.setBoolean(False)

        denormalized_viser_hub_x_offset = int(img.shape[1] / 2 * (properties.values.viser_hub_x_offset + 1))
        cv2.line(img, (denormalized_viser_hub_x_offset, 0), (denormalized_viser_hub_x_offset, int(img.shape[0])), (255, 255, 255), 1)

        NetworkTables.flush()
        outputStream.putFrame(img)
        yield


def main():
    loop = hub_loop()
    while True:
        next(loop)


if __name__ == '__main__':
    main()
