import cv2

from cvzone.FaceMeshModule import FaceMeshDetector
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = FaceMeshDetector(maxFaces=1)

while True:
    success, img = capture.read()
    img, faces = detector.findFaceMesh(img)
    cv2.imshow("Display Face Mesh", img)
    cv2.waitKey(1)
