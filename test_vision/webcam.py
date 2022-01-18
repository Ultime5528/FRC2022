import cv2
from balles import Balles

cam = cv2.VideoCapture(0)


while True:
    _, img = cam.read()
    cond, infoCercles = Balles(img, "rouge")

    if cond == True:
        for cercleX, cercleY, cercleHW in infoCercles:
            cv2.rectangle(img, (cercleX, cercleY), (cercleX + cercleHW, cercleY - cercleHW), (255, 255, 255), 3)

    cv2.imshow("webcam", img)
    if cv2.waitKey(10) == ord('q'): break

cam.release()
cv2.destroyAllWindows()