import cv2

from balles2 import Balles2

img = cv2.imread('C:/Users/filal/Desktop/marchandises/Balls/DSC01695.jpg')

# infoCercles = Balles(img, "rouge", 10, 50, 30, 50)
infoCercles = Balles2(img, "rouge", 0.5)

for cercleX, cercleY, cercleW, cercleH in infoCercles:
    cv2.rectangle(img, (cercleX, cercleY), (cercleX + cercleW, cercleY + cercleH), (255, 255, 255), 3)

cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
