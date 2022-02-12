import cv2
from balles import Balles
from balles2 import Balles2

cam = cv2.VideoCapture(0)

while True:
    _, img = cam.read()
    # infoCercles = Balles(img, "rouge", 10, 50, 30, 50)
    infoCercles = Balles2(img, "bleu", 0.25)

        
    for cercleX, cercleY, cercleW, cercleH in infoCercles:
            cv2.rectangle(img, (cercleX, cercleY), (cercleX + cercleW, cercleY + cercleH), (255, 255, 255), 3)

    cv2.imshow("webcam", img)
    if cv2.waitKey(10) == ord('q'): break

cam.release()
cv2.destroyAllWindows()