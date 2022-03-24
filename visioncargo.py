import numpy as np
import cv2
from networktables import NetworkTables
from cscore import CameraServer
from vision.color import Color
from vision.balldetection.algorithms import circularityMoments

W = 320
H = 240

class Cargo:
    def __init__(self, t, isred):
        self.x = t[0]
        self.y = t[1]
        self.w = t[2]
        self.h = t[3]

        self.nw = self.w / W
        self.nh = self.h / W

        self.r = (self.w + self.h)//4

        self.cx = self.x+self.w//2
        self.cy = self.y+self.h//2

        self.nx = (t[0] / W) * 2 - 1
        self.ny = 1 - (t[1] / H)

        # self.distsq = self.nx**2+self.ny**2

        self.isred = isred

def cargo_loop():
    nt_normx = NetworkTables.getEntry("/Vision/Cargo/Norm_X")
    nt_normy = NetworkTables.getEntry("/Vision/Cargo/Norm_Y")
    nt_normw = NetworkTables.getEntry("/Vision/Cargo/Norm_W")
    nt_isred = NetworkTables.getEntry("/Vision/Cargo/IsRed")

    cs = CameraServer.getInstance()
    cs.kBasePort = 1183
    cs.enableLogging()

    cargo_cam = cs.startAutomaticCapture(name="cargo_cam", path="/dev/v4l/by-id/usb-Microsoft_Microsoft®_LifeCam_HD-3000-video-index0")
    cargo_cam.setResolution(W, H)
    cargo_cam.setFPS(30)

    cvSink = cs.getVideo(camera=cargo_cam)

    outputStream = cs.putVideo("Cargo", W, H)

    img = np.zeros(shape=(H, W, 3), dtype=np.uint8)

    while True:
        ret, img = cvSink.grabFrame(img)
        if ret == 0:
            outputStream.notifyError(cvSink.getError())
            continue

        red_targets = [Cargo(c, True) for c in circularityMoments(img, Color.RED)]
        blue_targets = [Cargo(c, False) for c in circularityMoments(img, Color.BLUE)]

        targets = red_targets + blue_targets

        nt_normx.setDoubleArray([t.nx for t in targets])
        nt_normy.setDoubleArray([t.ny for t in targets])
        nt_normw.setDoubleArray([t.nw for t in targets])
        nt_isred.setBooleanArray([t.isred for t in targets])
        NetworkTables.flush()

        for t in targets:
            color = (255, 0, 0)
            if t.isred:
                color = (0, 0, 255)
            cv2.rectangle(img, (t.x, t.y), (t.x+t.w, t.y+t.h), color, 3)

        outputStream.putFrame(img)
        yield

def main():
    loop = cargo_loop()
    while True:
        next(loop)

if __name__ == '__main__':
    main()
