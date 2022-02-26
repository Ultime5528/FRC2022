import time

import threading
import numpy as np
import cv2
from networktables import NetworkTables
from cscore import CameraServer
from vision.dataset import Color
from vision.balldetection.algorithms import circularityMoments

isConnected = threading.Condition()
notified = [False]

def connectionListener(connected, info):
    with isConnected:
        notified[0] = True
        isConnected.notify()

def main():
    NetworkTables.initialize(server="127.0.0.1")
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

    with isConnected:
        print("Waiting for connection...")
        if not notified[0]:
            isConnected.wait()
    print("Connected!")

    nt_isredalliance = NetworkTables.getEntry("/FMSInfo/IsRedAlliance")
    isRedAlliance = nt_isredalliance.getBoolean(None)

    if isRedAlliance is not None:
        color = Color.RED if isRedAlliance else Color.BLUE
    else:
        raise Exception("Variable /FMSInfo/IsRedAlliance is not declared")

    nt_normx = NetworkTables.getEntry("Vision/Cargo/Norm_X")
    nt_normy = NetworkTables.getEntry("Vision/Cargo/Norm_Y")

    cs = CameraServer.getInstance()
    cs.enableLogging()

    camera = cs.startAutomaticCapture()
    camera.setResolution(320, 240) # TODO CHANGE
    camera.setFPS(30) # TODO CHANGE

    cvSink = cs.getVideo()

    outputStream = cs.putVideo("Cargo", 320, 240)

    img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

    while True:
        ret, img = cvSink.grabFrame(img)
        if ret == 0:
            outputStream.notifyError(cvSink.getError())
            continue

        targets = circularityMoments(img, color)

        nearest = max(targets, key=lambda t: t[0])

        norm_x = (nearest[0] / img.shape[1]) * 2 - 1
        norm_y = (nearest[1] / img.shape[0]) * 2 - 1

        nt_normx.setDouble(norm_x)
        nt_normy.setDouble(norm_y)

        for t in targets:
            cv2.circle(img, (t[2], t[3]), 3, (0, 0, 255), 3)

        cv2.circle(img, (nearest[2], nearest[3]), 3, (0, 255, 0), 3)
        outputStream.putFrame(img)

if __name__ == '__main__':
    main()
