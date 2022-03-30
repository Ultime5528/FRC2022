import cv2
import numpy as np
from cscore import CameraServer
from networktables import NetworkTables

from vision.balldetection.algorithms import circularityMoments, ResultHolder
from vision.color import Color

W = 320
H = 240
DEBUG = False


class Cargo:
    def __init__(self, t, isred):
        self.x = t[0]
        self.y = t[1]
        self.w = t[2]
        self.h = t[3]

        self.nw = self.w / W
        self.nh = self.h / H

        self.r = (self.w + self.h) // 4

        self.cx = self.x + self.w // 2
        self.cy = self.y + self.h // 2

        self.nx = (self.cx / W) * 2 - 1
        self.ny = 1 - (self.cy / H)

        # self.distsq = self.nx**2+self.ny**2

        self.isred = isred

    def __repr__(self):
        return f"Cargo(x={self.x}, y={self.y}, w={self.w}, h={self.h}, nw={self.nw}, nh={self.nh}, cx={self.cx}, cy={self.cy}, nx={self.nx}, ny={self.ny})"


def crop_center(img, x_min, x_max, y_min, y_max):
    h = img.shape[0]
    w = img.shape[1]
    return img[int(h * y_min): int(h * y_max), int(w * x_min): int(w * x_max)]


def mask_crop_center(img, x_min, x_max, y_min, y_max):
    h = img.shape[0]
    w = img.shape[1]
    x_min = int(w * x_min)
    x_max = int(w * x_max)
    y_min = int(h * y_min)
    y_max = int(h * y_max)
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(mask, (x_min, y_min), (x_max, y_max), 255, -1)
    return cv2.bitwise_and(img, img, mask=mask)


def cargo_loop():
    nt_normx = NetworkTables.getEntry("/Vision/Cargo/Norm_X")
    nt_normy = NetworkTables.getEntry("/Vision/Cargo/Norm_Y")
    nt_normw = NetworkTables.getEntry("/Vision/Cargo/Norm_W")
    nt_isred = NetworkTables.getEntry("/Vision/Cargo/IsRed")

    crop_x_min = NetworkTables.getEntry("/Properties/vision_cargo_crop_x_min")
    crop_x_max = NetworkTables.getEntry("/Properties/vision_cargo_crop_x_max")
    crop_y_min = NetworkTables.getEntry("/Properties/vision_cargo_crop_y_min")
    crop_y_max = NetworkTables.getEntry("/Properties/vision_cargo_crop_y_max")

    red_hsv_low = NetworkTables.getEntry("/Properties/vision_cargo_red_hsv_low")
    red_hsv_high = NetworkTables.getEntry("/Properties/vision_cargo_red_hsv_high")
    blue_hsv_low = NetworkTables.getEntry("/Properties/vision_cargo_blue_hsv_low")
    blue_hsv_high = NetworkTables.getEntry("/Properties/vision_cargo_blue_hsv_high")

    min_radius = NetworkTables.getEntry("/Properties/vision_cargo_min_radius")
    circularity_error = NetworkTables.getEntry("/Properties/vision_cargo_circularity_error")

    cs = CameraServer.getInstance()
    cs.enableLogging()

    cargo_cam = cs.startAutomaticCapture(
        name="cargo_cam",
        path="/dev/v4l/by-id/usb-HD_Camera_Manufacturer_HD_USB_Camera_SN0008-video-index0",
    )
    cargo_cam.setResolution(W, H)
    cargo_cam.setFPS(30)

    cvSink = cs.getVideo(camera=cargo_cam)

    outputStream = cs.putVideo("Cargo", W, H)

    if DEBUG:
        red_mask = ResultHolder()
        blue_mask = ResultHolder()
        redStream = cs.putVideo("red", W, H)
        blueStream = cs.putVideo("blue", W, H)
    else:
        red_mask = None
        blue_mask = None

    img = np.zeros(shape=(H, W, 3), dtype=np.uint8)

    while True:
        ret, img = cvSink.grabFrame(img)

        img = cv2.resize(img, (W, H))

        if ret == 0:
            outputStream.notifyError(cvSink.getError())
            continue

        img_crop = mask_crop_center(
            img,
            crop_x_min.getDouble(0.05),
            crop_x_max.getDouble(0.95),
            crop_y_min.getDouble(0.1),
            crop_y_max.getDouble(0.9),
        )

        hsv_thresholds = dict(
            red_hsv_low=red_hsv_low.getDoubleArray([]),
            red_hsv_high=red_hsv_high.getDoubleArray([]),
            blue_hsv_low=blue_hsv_low.getDoubleArray([]),
            blue_hsv_high=blue_hsv_high.getDoubleArray([]),
        )

        red_targets = [
            Cargo(c, True)
            for c in circularityMoments(
                img_crop,
                Color.RED,
                **hsv_thresholds,
                error=circularity_error.getDouble(0.2),
                minRadiusPerc=min_radius.getDouble(0.03),
                mask_result=red_mask,
            )
        ]
        blue_targets = [
            Cargo(c, False)
            for c in circularityMoments(
                img_crop,
                Color.BLUE,
                **hsv_thresholds,
                error=circularity_error.getDouble(0.2),
                minRadiusPerc=min_radius.getDouble(0.03),
                mask_result=blue_mask,
            )
        ]

        if DEBUG:
            redStream.putFrame(red_mask.result)
            blueStream.putFrame(blue_mask.result)

        targets = red_targets + blue_targets

        nt_normx.setDoubleArray([t.nx for t in targets])
        nt_normy.setDoubleArray([t.ny for t in targets])
        nt_normw.setDoubleArray([t.nw for t in targets])
        nt_isred.setBooleanArray([t.isred for t in targets])
        NetworkTables.flush()

        if DEBUG:
            img = img_crop

        for t in targets:
            color = (255, 0, 0)
            if t.isred:
                color = (0, 0, 255)
            cv2.rectangle(img, (t.x, t.y), (t.x + t.w, t.y + t.h), color, 1)

        outputStream.putFrame(img)
        yield


def main():
    loop = cargo_loop()
    while True:
        next(loop)


if __name__ == "__main__":
    main()
