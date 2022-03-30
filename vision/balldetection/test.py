import cv2

import algorithms
import balldetection

# img = cv2.imread('C:/Users/Tremb/OneDrive/Documents/coding/FRC/balldetection/20211119_095809.jpg')
# optimal_shape = 530
# h, w, _ = img.shape
# f = optimal_shape / w if w >= h else optimal_shape / h
# img = cv2.resize(img, (0, 0), fx=f, fy=f)
# print(img.shape)

cam = cv2.VideoCapture(0)

while True:
    _, img = cam.read()
    res1 = algorithms.houghCircles(img, balldetection.Color.BLUE)
    res2 = algorithms.circularity(img, balldetection.Color.BLUE)
    res3 = algorithms.circularityConvex(img, balldetection.Color.BLUE)
    res4 = algorithms.circularityMoments(img, balldetection.Color.BLUE)
    res5 = algorithms.circularityConvexMoments(img, balldetection.Color.BLUE)
    res6 = algorithms.RANSAC(img, balldetection.Color.BLUE)
    res7 = algorithms.cannyRANSAC(img, balldetection.Color.BLUE)

    for ballX, ballY, ballWH, _ in res1:
        cv2.rectangle(img, (ballX, ballY), (ballX + ballWH, ballY + ballWH), (0, 0, 255), 3)

    for ballX, ballY, ballWH, _ in res2:
        cv2.rectangle(img, (ballX, ballY), (ballX + ballWH, ballY + ballWH), (255, 0, 0), 3)

    for ballX, ballY, ballWH, _ in res3:
        cv2.rectangle(img, (ballX, ballY), (ballX + ballWH, ballY + ballWH), (0, 255, 0), 3)

    for ballX, ballY, ballWH, _ in res4:
        cv2.rectangle(img, (ballX, ballY), (ballX + ballWH, ballY + ballWH), (255, 255, 0), 3)

    for ballX, ballY, ballWH, _ in res5:
        cv2.rectangle(img, (ballX, ballY), (ballX + ballWH, ballY + ballWH), (255, 255, 255), 3)

    for ballX, ballY, ballWH, _ in res6:
        cv2.rectangle(img, (ballX, ballY), (ballX + ballWH, ballY + ballWH), (0, 255, 225), 3)

    for ballX, ballY, ballWH, _ in res7:
        cv2.rectangle(img, (ballX, ballY), (ballX + ballWH, ballY + ballWH), (255, 0, 255), 3)

    cv2.imshow("webcam", img)

    if cv2.waitKey(10) == 113: break

cam.release()
cv2.destroyAllWindows()
