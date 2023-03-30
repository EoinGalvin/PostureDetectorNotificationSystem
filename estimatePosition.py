# Capture frames from the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Convert the frame to grayscale and blur it
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)

    # Threshold the image to obtain a binary mask
    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]

    # Find the contours in the binary mask
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPRO
