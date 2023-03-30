import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np
from win11toast import notify


def getMidpoint(p1, p2):
    midPoint = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    return midPoint


def getSlope(p1, p2):
    rise = (p2[1] - p1[1])
    run = (p2[0] - p1[0])
    return rise, run


def eligibleNotificationChecker(value, message):
    if value >= 75:
        notify(message)
        return True
    else:
        return False


class UserPosition:
    centreOffset = None
    distance = None
    height = None
    eyeAngle = None

    def setCentreYOffset(self, leftEye, rightEye, img, pixelToRealRatio):
        centreOfEyes = getMidpoint(leftEye, rightEye)
        centreOfImage = (img.shape[1] // 2, img.shape[0] // 2)
        centreOffsetPixels = abs(centreOfImage[0] - centreOfEyes[0])

        self.centreOffset = int(centreOffsetPixels / pixelToRealRatio)

    def setDistance(self, leftEye, rightEye, realDistanceBetweenEyes, focalLength):
        pixelDistanceBetweenEyes = detector.findDistance(leftEye, rightEye)

        self.distance = int((realDistanceBetweenEyes * focalLength) / pixelDistanceBetweenEyes[0])

    def setHeight(self, levelWithWebcamYCoord, centreOfEyes, pixelToRealRatio):
        heightOffsetInPixels = levelWithWebcamYCoord - centreOfEyes[1]

        self.height = int(heightOffsetInPixels / pixelToRealRatio)

    def setEyeAngle(self, leftEye, rightEye):
        rise, run = getSlope(leftEye, rightEye)
        self.eyeAngle = int(abs(np.rad2deg(np.arctan2(rise, run))))

    def displayUserInformation(self):
        print("User height : " + str(self.height) + "cm")
        print("User Distance : " + str(self.distance) + "cm")
        print("User Centre offset : " + str(self.centreOffset) + "cm")
        print("User eye angle offset : " + str(self.eyeAngle) + "°")


class Notifications:
    heightCount = 0
    distanceCount = 0
    cOffsetCount = 0
    eyeAngleOffsetCount = 0
    user = None

    def __init__(self, user):
        if user is not None:
            self.user = user

    def heightTracker(self):
        if user.height <= -10 or user.height >= 10:
            self.heightCount += 1
        else:
            self.heightCount = 0

        if eligibleNotificationChecker(self.heightCount, "Height"):
            self.heightCount = 0

    def distanceTracker(self):
        if user.distance >= 40 or user.distance <= 15:
            self.distanceCount += 1
        else:
            self.distanceCount = 0

        if eligibleNotificationChecker(self.distanceCount, "Distance"):
            self.distanceCount = 0

    def centreOffsetTracker(self):
        if user.centreOffset >= 8:
            self.cOffsetCount += 1
        else:
            self.cOffsetCount = 0

        if eligibleNotificationChecker(self.cOffsetCount, "Centre Offset"):
            self.cOffsetCount = 0

    def eyeAngleTracker(self):
        if user.eyeAngle >= 10:
            self.eyeAngleOffsetCount += 1
        else:
            self.eyeAngleOffsetCount = 0

        if eligibleNotificationChecker(self.eyeAngleOffsetCount, "Eye Angle Offset"):
            self.eyeAngleOffsetCount = 0


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
detector = FaceMeshDetector(maxFaces=1)

user = UserPosition()
notifications = Notifications(user)

realDistanceBetweenEyes = 6.3
focalLength = 600

while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        leftEye = face[145]
        rightEye = face[374]

        centreOfEyes = getMidpoint(leftEye, rightEye)
        pixelToRealRatio = detector.findDistance(leftEye, rightEye)[0] / realDistanceBetweenEyes
        webcamLevelApproximation = img.shape[0] * 0.42

        user.setHeight(webcamLevelApproximation, centreOfEyes, pixelToRealRatio)
        user.setDistance(leftEye, rightEye, realDistanceBetweenEyes, focalLength)
        user.setCentreYOffset(leftEye, rightEye, img, pixelToRealRatio)
        user.setEyeAngle(leftEye, rightEye)

        notifications.heightTracker()
        notifications.distanceTracker()
        notifications.centreOffsetTracker()
        notifications.eyeAngleTracker()

        cvzone.putTextRect(img, f'Eye Angle: {int(user.eyeAngle)} degree',
                           (50, 30),
                           scale=1.5)

        cvzone.putTextRect(img, f'Distance: {int(user.distance)}cm',
                           (50, 70),
                           scale=1.5)

        cvzone.putTextRect(img, f'Height: {int(user.height)}cm',
                           (50, 110),
                           scale=1.5)

        cvzone.putTextRect(img, f'C-offset: {int(user.centreOffset)}cm',
                           (50, 150),
                           scale=1.5)


    cv2.imshow("Display User Data", img)
    cv2.waitKey(1)
