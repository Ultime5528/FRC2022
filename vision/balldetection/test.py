import cv2
import balldetection
import algorithms

img = cv2.imread('C:/Users/Tremb/OneDrive/Documents/coding/FRC/balldetection/20211119_095809.jpg')
optimal_shape = 530
h, w, _ = img.shape
f = optimal_shape / w if w >= h else optimal_shape / h
img = cv2.resize(img, (0, 0), fx=f, fy=f)
print(img.shape)
# res = algorithms.houghCircles(img, balldetection.Color.BLUE)0
# res = algorithms.circularityConvexMoments(img, balldetection.Color.BLUE)
# res = algorithms.RANSAC(img, balldetection.Color.BLUE)
res = algorithms.cannyRANSAC(img, balldetection.Color.RED)
for ballX, ballY, ballWH, _ in res:
    cv2.rectangle(img, (ballX, ballY), (ballX + ballWH, ballY + ballWH), (255, 255, 255), 3)

cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.destroyAllWindows()
