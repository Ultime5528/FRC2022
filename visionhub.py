import cv2
import numpy as np
from cscore import CameraServer
from networktables import NetworkTables

import properties

DEBUG = True
TOLERANCE = 1.5


class Target:
    def __init__(self, cnt):
        self.x, self.y, self.w, self.h = cv2.boundingRect(cnt)
        (_, _), (self.minW, self.minH), self.raw_angle = cv2.minAreaRect(cnt)
        self.angle = self.raw_angle
        if self.minW < self.minH:
            self.angle += 90
        self.cx = int(round(self.x + self.w / 2))
        self.cy = int(round(self.y + self.h / 2))
        self.area = cv2.contourArea(cnt)
        self.perimeter = cv2.arcLength(cnt, True)
        self.minArea = int(self.minW) * int(self.minH)
        self.rectangularity = self.area / self.minArea if self.minArea else 0.0
        self.adjacents = {self}

    def __repr__(self):
        return (
            f"Target(x={self.x}, y={self.y}, w={self.w}, h={self.h}, "
            f"minW={self.minW:.1f}, minH={self.minH:.1f}, "
            f"area={self.area:.1f}, minArea={self.minArea:.1f}, "
            f"rect={self.rectangularity:.2f}, raw_angle={self.raw_angle:.2f}, angle={self.angle:.2f})"
        )

    @property
    def minX(self):
        return min(map(lambda t: t.x, self.adjacents))

    @property
    def maxX(self):
        return max(map(lambda t: t.x + t.w, self.adjacents))

    @property
    def minY(self):
        return min(map(lambda t: t.y, self.adjacents))

    @property
    def maxY(self):
        return max(map(lambda t: t.y, self.adjacents))

    @property
    def score(self):
        return len(self.adjacents)

    def is_near(self, other: "Target") -> bool:
        left = min(self.adjacents, key=lambda t: t.x)
        right = max(self.adjacents, key=lambda t: t.x)
        maxH = max(map(lambda t: t.h, self.adjacents))
        minY = self.minY - TOLERANCE * maxH
        maxY = self.maxY + (TOLERANCE + 1) * maxH
        min_area = 0.25 * min(map(lambda t: t.w * t.h, self.adjacents))
        return ((left.x - TOLERANCE * left.w) <= other.cx <= (right.x + (TOLERANCE + 1) * right.w)) and (
                    minY <= other.cy <= maxY) and (other.w * other.h) >= min_area


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
        mask = cv2.dilate(mask, kernel, iterations=1)
        # mask = cv2.erode(mask, kernel, iterations=1)

        _, cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imshow('mask', mask)
        if DEBUG:
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            mask = cv2.drawContours(mask, cnts, -1, (0, 0, 255), 1)

        targets = []

        if cnts is not None:
            if DEBUG:
                print("==========")
                print("nb cnts :", len(cnts))

            for cnt in cnts:
                target = Target(cnt)

                if target.rectangularity >= properties.values.vision_hub_rectangularity_threshold and target.perimeter >= properties.values.vision_hub_perimeter_threshold:
                    x, y, w, h = cv2.boundingRect(cnt)
                    ratio = max(target.w, target.h) / min(target.w, target.h)
                    if 1.00 <= ratio <= 3.5:
                        targets.append(target)

                if DEBUG:
                    print("---")
                    print(target)

        if binStream:
            for target in targets:
                cv2.rectangle(mask, (target.x, target.y), (target.x + target.w, target.y + target.h), (0, 255, 255), 1)
            binStream.putFrame(mask)

        targets = sorted(targets, key=lambda t: t.x)

        for target in targets:
            for other in targets:
                if target.is_near(other):
                    target.adjacents.add(other)

        targets = list(filter(lambda t: 2 <= t.score <= 7, targets))

        if targets:
            bestTarget = max(targets, key=lambda t: t.score)

            if DEBUG:
                for target in bestTarget.adjacents:
                    cv2.circle(mask, (int(target.cx), int(target.cy)), 2, (0, 0, 255), 1)

            mean_x = (bestTarget.minX + bestTarget.maxX) / 2
            mean_y = (bestTarget.minY + bestTarget.maxY) / 2
            norm_x = (mean_x / img.shape[1]) * 2 - 1
            norm_y = (mean_y / img.shape[0]) * 2 - 1

            nt_normx.setDouble(norm_x)
            nt_normy.setDouble(norm_y)
            nt_found.setBoolean(True)

            cv2.circle(img, (int(mean_x), int(mean_y)), 3, (255, 0, 255), 5)
            cv2.rectangle(img, (int(bestTarget.minX), int(bestTarget.minY)), (int(bestTarget.maxX), int(bestTarget.maxY)), (0, 0, 255), 1)

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
