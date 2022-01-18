import cv2
from balles import Balles

img = cv2.imread('C:/Users/filal/Desktop/marchandises/Balls/20211119_095925.jpg')


cond, infoCercles = Balles(img, "rouge")

if cond == True:
    for cercleX, cercleY, cercleHW in infoCercles:
        cv2.rectangle(img, (cercleX, cercleY), (cercleX + cercleHW, cercleY - cercleHW), (255, 255, 255), 3)

cv2.imshow("webcam", img)
cv2.waitKey(0)
cv2.destroyAllWindows()