import time

import threading
import numpy as np
import cv2
from networktables import NetworkTables
from cscore import CameraServer
from vision.color import Color
from vision.balldetection.algorithms import circularityMoments

isConnected = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    with isConnected:
        notified[0] = True
        isConnected.notify()

def cargo_loop():
    NetworkTables.initialize(server="10.55.28.2")
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

    # with isConnected:
    #     print("Waiting for connection...")
    #     if not notified[0]:
    #         isConnected.wait()
    # print("Connected!")

    nt_isredalliance = NetworkTables.getEntry("/FMSInfo/IsRedAlliance")
    isRedAlliance = nt_isredalliance.getBoolean(None)

    if isRedAlliance is not None:
        color = Color.RED if isRedAlliance else Color.BLUE
    else:
        color = Color.RED
        print("WARNING: Variable /FMSInfo/IsRedAlliance is not declared")
        # raise Exception("Variable /FMSInfo/IsRedAlliance is not declared")

    nt_normx = NetworkTables.getEntry("/Vision/Cargo/Norm_X")
    nt_normy = NetworkTables.getEntry("/Vision/Cargo/Norm_Y")

    cs = CameraServer.getInstance()
    cs.kBasePort = 1183
    cs.enableLogging()

    cargo_cam = cs.startAutomaticCapture(name="cargo_cam", path="/dev/v4l/by-id/usb-Microsoft_Microsoft®_LifeCam_HD-3000-video-index0")
    cargo_cam.setResolution(320, 240) # TODO CHANGE
    cargo_cam.setFPS(30) # TODO CHANGE

    cvSink = cs.getVideo(camera=cargo_cam)

    outputStream = cs.putVideo("Cargo", 320, 240)

    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    while True:
        ret, img = cvSink.grabFrame(img)
        if ret == 0:
            outputStream.notifyError(cvSink.getError())
            continue

        targets = circularityMoments(img, color)

        if targets:
            nearest = max(targets, key=lambda t: t[0])

            norm_x = (nearest[0] / img.shape[1]) * 2 - 1
            norm_y = (nearest[1] / img.shape[0]) * 2 - 1

            nt_normx.setDouble(norm_x)
            nt_normy.setDouble(norm_y)
            NetworkTables.flush()


            for t in targets:
                cv2.circle(img, (t[2], t[3]), 3, (0, 0, 255), 3)

            cv2.circle(img, (nearest[2], nearest[3]), 3, (0, 255, 0), 3)
        outputStream.putFrame(img)
        yield

def main():
    loop = cargo_loop()
    while True:
        next(loop)

if __name__ == '__main__':
    main()
