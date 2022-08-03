import cv2 as cv

frameWidth = 640
frameHeight = 480

cap = cv.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150)

while True:
    success, img = cap.read()
    cv.imshow('Result',img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break