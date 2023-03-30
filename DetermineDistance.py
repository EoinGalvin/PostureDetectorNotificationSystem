import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector


def getMidpoint(p1, p2):
    return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = FaceMeshDetector(maxFaces=1)

while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        pointLeft = face[145]
        pointRight = face[374]

        centreOfEyes = getMidpoint(pointLeft, pointRight)
        #print("center point between eyes is : " + str(centreOfEyes[0]))

        print("Y coordinate of eyes: " + str(centreOfEyes[1]))
        w, _ = detector.findDistance(pointLeft, pointRight)
        W = 6.3 # cm

        # Finding distance
        f = 600
        d = (W * f) / w

        # Calculate the position of the center of the webcam frame
        centre_x, centre_y = img.shape[1] // 2, img.shape[0] // 2

        #print(" centre x of image is : " + str(centre_x))

        centreOffset = abs(centre_x - centreOfEyes[0])
        #print("Offset from centre of image : " + str(centreOffset))

        # dist_px = ((left_eye_pos[0] - center_x) ** 2 + (left_eye_pos[1] - center_y) ** 2) ** 0.5

        cvzone.putTextRect(img, f'Distance: {int(d)}cm',
                           (face[10][0] - 100, face[10][1] - 50),
                           scale=2.5)

    cv2.imshow("Display Distance", img)

    cv2.waitKey(1)
